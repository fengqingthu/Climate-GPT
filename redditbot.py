import praw
import re
import time
import threading
from climategpt import get_response
from credentials import client_id as CLIENT_ID, client_secret as CLIENT_SECRET, r_password as PASSWORD

# Replace with your own values
USERNAME = "ClimateGPT"
USER_AGENT = "macos:climatebot:1.0 (by /u/ClimateGPT)"

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent=USER_AGENT,
)

def monitor_thread(thread_url: str):
    # Get the thread ID from the URL
    match = re.match(r"https://www\.reddit\.com/r/\w+/comments/(\w+)/", thread_url)
    thread_id = match.group(1)

    # Get the thread object
    thread = reddit.submission(id=thread_id)

    # Monitor the thread for new comments
    while True:
        thread.comments.replace_more(limit=None)
        for comment in thread.comments.list():
            if re.search(r"climate change", comment.body, re.IGNORECASE):
                reply_text = get_response(comment.body)
                comment.reply(reply_text)
                print(f"Replied to comment by u/{comment.author}: {reply_text}")
        time.sleep(60)

# Define the monitoring function
def monitor_thread(thread_url: str):
    # Get the thread ID from the URL
    match = re.match(r"https://www\.reddit\.com/r/\w+/comments/(\w+)/", thread_url)
    thread_id = match.group(1)

    # Get the thread object
    thread = reddit.submission(id=thread_id)

    last_comment_time = None

    # Monitor the thread for new comments
    while True:
        print("checking reddit thread...")
        thread.comments.replace_more(limit=None)
        for comment in thread.comments.list():
            # Check if the comment was published after the last comment we processed
            if last_comment_time is None or comment.created_utc > last_comment_time:
                # Matching key word
                if re.search(r"climate change", comment.body, re.IGNORECASE):
                    reply_text = get_response(comment.body)
                    comment.reply(reply_text)
                    print(f"Replied to comment by u/{comment.author}: {reply_text}")
        time.sleep(60)

# Start the monitoring function in a separate thread running in the background
def start_monitor_thread(thread_url: str):
    t = threading.Thread(target=monitor_thread, args=(thread_url,))
    t.start()