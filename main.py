import argparse

import praw
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

parser = argparse.ArgumentParser()
parser.add_argument("--reddit-client-id", type=str, help="Reddit Client ID")
parser.add_argument("--reddit-client-secret", type=str, help="Reddit Client Secret")
parser.add_argument("--reddit-username", type=str, help="Reddit Username")
parser.add_argument("--reddit-password", type=str, help="Reddit Password")
parser.add_argument("--subreddit-name", type=str, default="MachineLearning", help="Subreddit Name")
parser.add_argument("--n-posts", type=int, default=20, help="Max Posts Number")
parser.add_argument("--slack-api-token", type=str, help="Slack API Token")
parser.add_argument("--slack-channel-id", type=str, help="Slack Channel ID")
args = parser.parse_args()

reddit = praw.Reddit(
    client_id=args.reddit_client_id,
    client_secret=args.reddit_client_secret,
    user_agent="script by /u/{}".format(args.reddit_username),
    username=args.reddit_username,
    password=args.reddit_password,
)

subreddit = reddit.subreddit(args.subreddit_name)

post_titles = []
for submission in subreddit.hot(limit=args.n_posts):
    if submission.stickied:
        continue

    post_title = f"<{submission.url}|{submission.title}> [Upvotes {submission.score}]"
    post_titles.append((submission.score, post_title))

slack_messages = [f"*Today's Hot Posts of {args.subreddit_name} Subreddit*\n"]
slack_messages += [f"{idx + 1}. {title}" for idx, (_, title) in enumerate(post_titles)]

client = WebClient(token=args.slack_api_token)
text = "\n".join(slack_messages)

try:
    response = client.chat_postMessage(channel=args.slack_channel_id, text=text)
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f'Got an error: {e.response["error"]}')
