"""
Official APIs for ChatGPT using OpenAIAuth, essentially chat.openai.com
Reference: https://github.com/acheong08/ChatGPT
"""
import asyncio
import json
import os

import httpx
import requests
import tiktoken
from OpenAIAuth.OpenAIAuth import OpenAIAuth

ENCODER = tiktoken.get_encoding("gpt2")


def get_max_tokens(prompt: str) -> int:
    """
    Get the max tokens for a prompt
    """
    return 4000 - len(ENCODER.encode(prompt))


class Message:
    """
    A single exchange between the user and the bot
    """

    def __init__(self, text: str, author: str) -> None:
        self.text: str = text
        self.author: str = author


class Conversation:
    """
    A single conversation
    """

    def __init__(self) -> None:
        self.messages: list[Message] = []


CONVERSATION_BUFFER: int = int(os.environ.get("CONVERSATION_BUFFER") or 1500)


class Conversations:
    """
    Conversation handler
    """

    def __init__(self) -> None:
        self.conversations: dict[str][Conversation] = {}

    def add_message(self, message: Message, conversation_id: str) -> None:
        """
        Adds a message to a conversation
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = Conversation()
        self.conversations[conversation_id].messages.append(message)

    def get(self, conversation_id: str) -> str:
        """
        Builds a conversation string from a conversation id
        """
        if conversation_id not in self.conversations:
            return ""
        # Build conversation string from messages and check if it's too long
        conversation = ""
        for message in self.conversations[conversation_id].messages:
            conversation += f"{message.author}: {message.text}<|im_sep|>\n\n"
        if len(ENCODER.encode(conversation)) > 4000 - CONVERSATION_BUFFER:
            self.purge_history(conversation_id)
            return self.get(conversation_id)
        return conversation

    def purge_history(self, conversation_id: str, num: int = 1):
        """
        Remove oldest messages from a conversation
        """
        if conversation_id not in self.conversations:
            return
        self.conversations[conversation_id].messages = self.conversations[
            conversation_id
        ].messages[num:]

    def rollback(self, conversation_id: str, num: int = 1):
        """
        Remove latest messages from a conversation
        """
        if conversation_id not in self.conversations:
            return
        self.conversations[conversation_id].messages = self.conversations[
            conversation_id
        ].messages[:-num]

    def remove(self, conversation_id: str) -> None:
        """
        Removes a conversation
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]


BASE_PROMPT = (
    os.environ.get("BASE_PROMPT")
    or """You are ChatGPT, a large language model by OpenAI. Respond conversationally\n\n\n"""
)

PROXY_URL = os.environ.get("PROXY_URL") or "https://chat.duti.tech"


class Chatbot:
    """
    Handles everything seamlessly
    """

    def __init__(
        self,
        email: str,
        password: str,
        paid: bool = False,
        proxy=None,
        insecure: bool = False,
        session_token: str = None,
    ) -> None:
        self.proxy = proxy
        self.email: str = email
        self.password: str = password
        self.session_token = session_token
        self.insecure: bool = insecure
        self.api_key: str
        self.paid: bool = paid
        self.conversations = Conversations()
        self.login(email, password, proxy, insecure, session_token)

    async def ask_async(self, prompt: str, conversation_id: str = None) -> dict:
        """
        Gets a response from the API
        """
        if conversation_id is None:
            conversation_id = "default"
        self.conversations.add_message(
            Message(prompt, "User"),
            conversation_id=conversation_id,
        )
        conversation: str = self.conversations.get(conversation_id)
        # Build request body
        body = self.__get_config()
        body["prompt"] = BASE_PROMPT + conversation + "ChatGPT: "
        body["max_tokens"] = get_max_tokens(conversation)
        async with httpx.AsyncClient(proxies=self.proxy if self.proxy else None).stream(
            method="POST",
            url=PROXY_URL + "/completions",
            data=json.dumps(body),
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=1080,
        ) as response:
            full_result = ""
            async for line in response.aiter_lines():
                if response.status_code == 429:
                    print("error: " + "Too many requests")
                    raise Exception("Too many requests")
                elif response.status_code == 523:
                    print(
                        "error: " + "Origin is unreachable. Ensure that you are authenticated and are using the correct pricing model.")
                    raise Exception(
                        "Origin is unreachable. Ensure that you are authenticated and are using the correct pricing model.")
                elif response.status_code == 503:
                    print("error: " + "OpenAI error!")
                    raise Exception("OpenAI error!")
                elif response.status_code != 200:
                    print("error: " + "Unknown error")
                    raise Exception("Unknown error")
                line = line.strip()
                if line == "\n" or line == "":
                    continue
                if line == "data: [DONE]":
                    break
                try:
                    # Remove "data: " from the start of the line
                    data = json.loads(line[6:])
                    if data is None:
                        continue
                    full_result += data["choices"][0]["text"].replace(
                        "<|im_end|>", "")
                    if "choices" not in data:
                        continue
                    yield data
                except json.JSONDecodeError:
                    continue
            self.conversations.add_message(
                Message(full_result, "ChatGPT"),
                conversation_id=conversation_id,
            )

    def __get_config(self) -> dict:
        return {
            "temperature": float(os.environ.get("TEMPERATURE") or 0.5),
            "top_p": float(os.environ.get("TOP_P") or 1),
            "stop": ["<|im_end|>", "<|im_sep|>"],
            "presence_penalty": float(os.environ.get("PRESENCE_PENALTY") or 1.0),
            "paid": self.paid,
            "stream": True,
        }

    def login(self, email, password, proxy, insecure, session_token) -> None:
        """
        Login to the API
        """
        if not insecure:
            auth = OpenAIAuth(email_address=email,
                              password=password, proxy=proxy)
            if session_token:
                auth.session_token = session_token
                auth.get_access_token()
                self.api_key = auth.access_token
                if self.api_key is None:
                    self.session_token = None
                    self.login(email, password, proxy, insecure, None)
                return
            auth.begin()
            self.session_token = auth.session_token
            self.api_key = auth.access_token
        else:
            auth_request = requests.post(
                PROXY_URL + "/auth",
                json={"email": email, "password": password},
                timeout=10,
            )
            self.api_key = auth_request.json()["accessToken"]

    def ask(self, prompt: str, conversation_id: str = None) -> str:
        """
        Sync API for chatbot
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = []

        async def collect_result():
            async for line in self.ask_async(prompt, conversation_id):
                result.append(line["choices"][0]
                              ["text"].replace("<|im_end|>", ""))
        loop.run_until_complete(collect_result())

        response = "".join(result).strip()
        print("prompt=" + prompt + "\nresponse=" + response)
        return response
