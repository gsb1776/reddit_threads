# Use PRAW to access Reddit info
# See docs for information: https://praw.readthedocs.io/en/latest/code_overview/reddit_instance.html
# https://praw.readthedocs.io/en/latest/code_overview/models/redditor.html

import praw

reddit = praw.Reddit(
    client_id="q33sziEQUMFF51P9IrtRHw",
    client_secret="xxNns4HmThugUzy6-o8LqsF8IY9W9A",
    user_agent="userinfo",
)

print(reddit.user.me())

# Iterate through submissions
for submission in reddit.subreddit("test").hot(limit=10):
    print(submission.title)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
