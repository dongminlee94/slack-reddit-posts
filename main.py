"""Main script to collect Reddit posts, summarize them using AI, and send to Slack."""

import argparse

import yaml
from tqdm import tqdm

from src.collector import RedditCollector
from src.llm import GenAIClient
from src.slack import SlackNotifier

parser = argparse.ArgumentParser()
parser.add_argument("--reddit-client-id", type=str, help="Reddit Client ID")
parser.add_argument("--reddit-client-secret", type=str, help="Reddit Client Secret")
parser.add_argument("--reddit-username", type=str, help="Reddit Username")
parser.add_argument("--reddit-password", type=str, help="Reddit Password")
parser.add_argument("--subreddit-name", type=str, help="Subreddit Name")
parser.add_argument("--n-posts", type=int, default=20, help="Max Posts Number")
parser.add_argument("--genai-api-key", type=str, help="Google GenAI API Key")
parser.add_argument("--slack-api-tokens", type=str, help="Slack API Tokens")
parser.add_argument("--slack-channel-ids", type=str, help="Slack Channel IDs")
args = parser.parse_args()

# Load system instruction from YAML file
with open("./prompt.yaml") as fp:
    system_instruction = yaml.safe_load(fp)["system"]

# Initialize Reddit Collector
reddit_collector = RedditCollector(
    client_id=args.reddit_client_id,
    client_secret=args.reddit_client_secret,
    username=args.reddit_username,
    password=args.reddit_password,
)

# Collect Reddit posts
posts_for_main, submissions_to_summarize = reddit_collector.collect_hot_posts(
    subreddit_name=args.subreddit_name, n_posts=args.n_posts
)

# Prepare the main Slack message text
main_slack_messages = [f"*Today's Hot Posts of {args.subreddit_name} Subreddit*\n"]
main_slack_messages += [f"{idx + 1}. {post}" for idx, post in enumerate(posts_for_main)]
main_message_text = "\n".join(main_slack_messages)

# Initialize LLM Client
genai_client = GenAIClient(
    api_key=args.genai_api_key, model="gemini-2.5-flash-preview-04-17", response_mime_type="text/plain"
)

# Generate summaries for each collected Reddit post.
summaries_for_threads = []
for idx, data in enumerate(tqdm(submissions_to_summarize, desc="Summarizing Posts")):
    # Generate a summary for the current post's content using the GenAI client.
    summary = genai_client.create_content(
        contents=[data["contents"]],
        system_instruction=system_instruction,
    )

    # Format the summary with the post title for the Slack thread.
    thread_summary_text = f"*{idx + 1}. {data['title']}*\n\n{summary}"
    summaries_for_threads.append(thread_summary_text)

# Split the comma-separated Slack tokens and channel IDs into lists.
slack_api_tokens = args.slack_api_tokens.split(",")
slack_channel_ids = args.slack_channel_ids.split(",")

# Iterate through each pair of Slack token and channel ID.
for token, channel_id in zip(slack_api_tokens, slack_channel_ids, strict=False):
    # Initialize the SlackNotifier
    slack_notifier = SlackNotifier(token=token)

    # Send the main message (list of posts) to the current channel and get its timestamp.
    main_message_ts = slack_notifier.send_main_message(channel_id=channel_id, text=main_message_text)

    # Send each summary as a threaded message under the main post.
    for thread_text in summaries_for_threads:
        slack_notifier.send_thread_message(
            channel_id=channel_id,
            text=thread_text,
            thread_ts=main_message_ts,
        )
