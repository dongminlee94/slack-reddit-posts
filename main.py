"""Main script to collect Reddit posts, summarize them using AI, and send to Slack."""

import argparse
import ast
import json

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
submissions_data = reddit_collector.collect_hot_posts(
    subreddit_name=args.subreddit_name, n_posts=args.n_posts
)

# Initialize LLM Client
genai_client = GenAIClient(
    api_key=args.genai_api_key, model="gemini-2.5-flash-preview-04-17", response_mime_type="application/json"
)

# Generate summaries for each collected Reddit post.
summaries_data = {}
for idx, data in enumerate(tqdm(submissions_data, desc="Summarizing Posts")):
    # Generate a summary for the current post's content using the GenAI client.
    response = genai_client.generate_content_with_retry(
        contents=[data["contents"]],
        system_instruction=system_instruction,
        temperature=0.5,
        top_p=0.5,
    )

    response_text = response.text

    print(f"idx: {idx}\n, response_text: {response_text}\n\n")

    if response_text is None:
        raise ValueError(
            f"No text content received from LLM for post idx {idx}: "
            f"{data['title']}. Cannot parse None as JSON."
        )

    try:
        summary = json.loads(response_text)
    except json.JSONDecodeError:
        summary = ast.literal_eval(response_text)
    except Exception as e:
        raise ValueError(f"JSON parsing failed: {response_text}") from e

    # Format the summary with the post title for the Slack message.
    three_line_summary = "\n".join(summary["세줄 요약"])
    summaries_data[idx] = {
        "main_message_text": f"*{idx + 1}. {data['title']}*\n\n{three_line_summary}",
        "thread_message_text": f"*본문 요약*\n{summary['본문 요약']}\n\n*댓글 요약*\n{summary['댓글 요약']}",
    }

# Split the comma-separated Slack tokens and channel IDs into lists.
slack_api_tokens = args.slack_api_tokens.split(",")
slack_channel_ids = args.slack_channel_ids.split(",")

# Iterate through each pair of Slack token and channel ID.
for token, channel_id in zip(slack_api_tokens, slack_channel_ids, strict=False):
    # Initialize the SlackNotifier
    slack_notifier = SlackNotifier(token=token)

    # Send the title Slack message text
    title_message_text = f"*Today's Hot Posts of {args.subreddit_name} Subreddit*\n"
    slack_notifier.send_main_message(channel_id=channel_id, text=title_message_text)

    # Send each summary to Slack
    for data in summaries_data.values():
        main_message_ts = slack_notifier.send_main_message(
            channel_id=channel_id, text=data["main_message_text"]
        )

        slack_notifier.send_thread_message(
            channel_id=channel_id,
            text=data["thread_message_text"],
            thread_ts=main_message_ts,
        )
