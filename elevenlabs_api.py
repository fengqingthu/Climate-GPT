"""ElevenLabs text to speech API wrappers"""
import requests
import abc
from threading import Lock
from credentials import eleven_lab_api_key
import base64

PLACEHOLDERS = {"your-voice-id"}


class VoiceBase():
    """
    Base class for all voice classes.
    """

    def __init__(self):
        """
        Initialize the voice class.
        """
        self._url = None
        self._headers = None
        self._api_key = None
        self._voices = []
        self._mutex = Lock()
        self._setup()

    @abc.abstractmethod
    def _setup(self) -> None:
        """
        Setup the voices, API key, etc.
        """
        pass

    @abc.abstractmethod
    def _speech(self, text: str, voice_index: int = 0) -> bool:
        """
        Play the given text.

        Args:
            text (str): The text to play.
        """
        pass


class ElevenLabsSpeech(VoiceBase):
    """ElevenLabs speech class"""

    def _setup(self) -> None:
        """Set up the voices, API key, etc.

        Returns:
            None: None
        """
        default_voices = ["21m00Tcm4TlvDq8ikWAM", "AZnzlk1XvdvUeBnXmlld",
                          "EXAVITQu4vr4xnSDxMaL", "ErXwobaYiN019PkySvjV",
                          "MF3mGyEYCl7XYWbV9V6O", "TxGEqnHWrfWFTfGW9XjX",
                          "VR6AewLTigWG4xSOukaG", "pNInz6obpgDQGcFmaJgB",
                          "yoZ06aMxZJJ28mfd3POQ"]
        # voice_options = {
        #     "Rachel": "21m00Tcm4TlvDq8ikWAM",
        #     "Domi": "AZnzlk1XvdvUeBnXmlld",
        #     "Bella": "EXAVITQu4vr4xnSDxMaL",
        #     "Antoni": "ErXwobaYiN019PkySvjV",
        #     "Elli": "MF3mGyEYCl7XYWbV9V6O",
        #     "Josh": "TxGEqnHWrfWFTfGW9XjX",
        #     "Arnold": "VR6AewLTigWG4xSOukaG",
        #     "Adam": "pNInz6obpgDQGcFmaJgB",
        #     "Sam": "yoZ06aMxZJJ28mfd3POQ",
        # }
        self._headers = {
            "Content-Type": "application/json",
            "xi-api-key": eleven_lab_api_key,
        }
        self._voices = default_voices.copy()

        # self._use_custom_voice(cfg.elevenlabs_voice_1_id, 0)
        # self._use_custom_voice(cfg.elevenlabs_voice_2_id, 1)

    def _use_custom_voice(self, voice, voice_index) -> None:
        """Use a custom voice if provided and not a placeholder

        Args:
            voice (str): The voice ID
            voice_index (int): The voice index

        Returns:
            None: None
        """
        # Placeholder values that should be treated as empty
        if voice and voice not in PLACEHOLDERS:
            self._voices[voice_index] = voice

    def _speech(self, text: str, voice_index: int = 0) -> bool:
        """Speak text using elevenlabs.io's API

        Args:
            text (str): The text to speak
            voice_index (int, optional): The voice to use. Defaults to 0.

        Returns:
            bool: True if the request was successful, False otherwise
        """
        tts_url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{self._voices[voice_index]}"
        )
        response = requests.post(
            tts_url, headers=self._headers, json={"text": text})

        if response.status_code == 200:
            # with open("speech.mpeg", "wb") as f:
            #     f.write(response.content)
            # playsound("speech.mpeg", True)
            # os.remove("speech.mpeg")
            response.close()
            return True
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.content)
            return False

    def synthesize_speech(self, text: str, voice_index: int = 0) -> str:
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self._voices[voice_index]}"
        response = requests.post(
            tts_url, headers=self._headers, json={"text": text})

        if response.status_code == 200:
            audio_data = response.content
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            audio_url = f"data:audio/mpeg;base64,{audio_base64}"
            return audio_url
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.content)
            return ''
