import praw
import re
import time
import random
import threading
from climategpt import get_response
from credentials import client_id as CLIENT_ID, client_secret as CLIENT_SECRET, r_password as PASSWORD

# Replace with your own values
USERNAME = "ClimateGPT"
USER_AGENT = "macos:climatebot:1.0 (by /u/ClimateGPT)"
MAX_CHECK_TIMES = 1000

try:
    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
        user_agent=USER_AGENT,
    )
except Exception as e:
    print("Fail to initialize reddit instance!")
    reddit = None


def monitor_thread(thread_id: str):
    try:
        thread = reddit.submission(id=thread_id)
        last_comment_time = None
    except Exception as e:
        # return early here
        return

    # Monitor the thread for new comments
    print(f"start checking reddit thread {thread_id}...")
    check_counter = 0
    while check_counter < MAX_CHECK_TIMES:
        check_counter += 1
        thread.comments.replace_more(limit=None)
        for comment in thread.comments.list():
            # Check if the comment was published after the last comment we have seen
            if last_comment_time is None or comment.created_utc > last_comment_time:
                last_comment_time = comment.created_utc

                # print("==========\n" + "is_root:" + str(comment.is_root) + "\nbody:" + comment.body +
                #       "\nauthor:" + str(comment.author) + "\n==========")

                # Check for others' comments that are not responded yet
                if comment.author != reddit.user.me() and not any(reply.author == reddit.user.me() for reply in comment.replies):
                    # Simply reply all comments
                    if True or re.search(r"climate change", comment.body, re.IGNORECASE):
                        reply_text = get_response(comment.body)
                        comment.reply(reply_text)
                        print(
                            f"Replied to comment by u/{comment.author}: {reply_text}")
        time.sleep(random.randint(30, 180))


# Start the monitoring function in a separate thread running in the background and return quickly
def start_monitor_thread(thread_url: str):
    try:
        match = re.match(
            r"https://www\.reddit\.com/r/\w+/comments/(\w+)/", thread_url)
        thread_id = match.group(1)
        t = threading.Thread(target=monitor_thread, args=(thread_id,))
        t.start()
        return f"Start monitoring reddit thread id={thread_id}..."
    except Exception as e:
        return "Sorry, there is a problem with the input url"
