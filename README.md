# Slack Reddit Posts

<img width="1143" src="https://github.com/Curt-Park/reddit-posts-to-slack/assets/14961526/14315a30-3285-433c-9a2a-5f4387e5814b">

This repository introduces a trigger that automatically sends hot posts from specified subreddits to a designated Slack channel.

## Preparation

### Reddit

1. Sign up for a Reddit account. Ensure that your `username` and `password` are registered.
2. Create [a Reddit application](https://www.reddit.com/prefs/apps). **Important: Select "script" as the application type from the available options (web app, installed app, script).**
3. Note down the `client id` and `client secret` values.
4. Set up the following secrets in this repository:
    - `REDDIT_CLIENT_ID`
    - `REDDIT_CLIENT_SECRET`
    - `REDDIT_USERNAME`
    - `REDDIT_PASSWORD`
5. Add the names of the subreddits to `.github/workflows/slack-reddit-posts.yaml`.

### Google GenAI API Key

1. Sign up for [a Google Cloud account](https://console.cloud.google.com/home/dashboard) if you don't already have one.
2. Enable the GenAI API in the Google Cloud Console.
3. Create a new API key from the credentials section.
4. Set up the following secret in this repository:
  - `GENAI_API_KEY`

### Slack

1. Create [a slack application](https://api.slack.com/apps).
2. Install the application to your Slack workspace.
3. In `OAuth & Permissions`, add `chat:write` to the `Bot Token Scopes`.
4. Create a new channel and add the application to it.
5. Set up the following secrets in this repository:
    - `SLACK_API_TOKENS`
    - `SLACK_CHANNEL_IDS`

## Usage

```bash
$ python main.py -h

usage: main.py [-h]
               [--reddit-client-id REDDIT_CLIENT_ID]
               [--reddit-client-secret REDDIT_CLIENT_SECRET]
               [--reddit-username REDDIT_USERNAME]
               [--reddit-password REDDIT_PASSWORD]
               [--subreddit-name SUBREDDIT_NAME]
               [--n-posts N_POSTS]
               [--genai-api-key GENAI_API_KEY]
               [--slack-api-tokens SLACK_API_TOKENS]
               [--slack-channel-ids SLACK_CHANNEL_IDS]

options:
  -h, --help            show this help message and exit
  --reddit-client-id REDDIT_CLIENT_ID               Reddit Client ID
  --reddit-client-secret REDDIT_CLIENT_SECRET       Reddit Client Secret
  --reddit-username REDDIT_USERNAME                 Reddit Username
  --reddit-password REDDIT_PASSWORD                 Reddit Password
  --subreddit-name SUBREDDIT_NAME                   Subreddit Name
  --n-posts N_POSTS                                 Max Posts Number
  --genai-api-key GENAI_API_KEY                     Google GenAI API Key
  --slack-api-tokens SLACK_API_TOKENS               Slack API Toekns
  --slack-channel-ids SLACK_CHANNEL_IDS             Slack Channel IDs
```

## References

- https://github.com/Curt-Park/reddit-posts-to-slack
- https://velog.io/@iamnotwhale/praw%EB%A1%9C-%EB%A0%88%EB%94%A7-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0
- https://gengminy.tistory.com/52
