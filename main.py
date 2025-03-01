# Use PRAW to access Reddit info
# See docs for information: https://praw.readthedocs.io/en/latest/code_overview/reddit_instance.html
# https://praw.readthedocs.io/en/latest/code_overview/models/redditor.html

import praw
import pandas as pd
import requests
import time
import json

reddit = praw.Reddit(
    client_id="q33sziEQUMFF51P9IrtRHw",
    client_secret="xxNns4HmThugUzy6-o8LqsF8IY9W9A",
    user_agent="userinfo",
)

print(reddit.user.me())

# List target subreddits
subreddits = ["politics", "economiccollapse", "antiwork"]
subreddits = [item.lower() for item in subreddits]

# Set some parameters
time_limit = "year"
count = 3

# Subreddit info will be stored as a dataframe with:
# top_subs, a dict with ["subreddit": karma]
# size
cols = ["sub_name", "top_subs", "size"]
subs = pd.DataFrame(columns=cols)


# Iterate through subreddits
for sub in subreddits:
    # Grab all authors

    subreddit = reddit.subreddit(sub)
    authors = []
    for submission in subreddit.top(time_filter = time_limit, limit=count):
        authors.append(submission.author)
    # Iterate through authors, getting their top subreddits and their karma 
    top_subs = {}
    for author in authors:
        # Get the top subreddits - COULD BE BLOCKED, need a check for this
        url = "https://www.reddit.com/user/" + author.name + "/top_karma_subreddits.json"
        time.sleep(1)
        response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
        # Load data as json 
        data = json.loads(response.text)
        # Iterate through all communities and add tuple
        if data is not None and data != {}:
            # Iterate by community
            for community in data["data"]:
                # Avoid double counting
                if community["display_name"].lower() != sub:
                    #print(community["display_name"])
                    #print(community)
                    name = community["display_name"].lower()
                    karma = community["link_karma"] + community["comment_karma"]
                    if name in top_subs:
                        # Update stats
                        top_subs[name] += karma
                    else:
                        # Or create entry
                        top_subs[name] = (karma)
    print(top_subs)
    # sort it
    top_subs = {k: v for k, v in sorted(top_subs.items(), key=lambda item: item[1], reverse=True)}
    # Get the user count for the subreddit
    url = "https://www.reddit.com/r/" + sub + "/about.json"
    time.sleep(1)
    response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
    data = json.loads(response.text)["data"]
    new_row = (sub, top_subs, data["subscribers"])
    subs.loc[len(subs)] = new_row
print(subs)
# Save
subs.to_csv('query.csv', index=False)