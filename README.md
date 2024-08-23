# Slack Reddit Posts

subreddit의 hot post들을 특정 슬랙 채널로 보내는 트리거를 소개합니다.

## Preparation

### Reddit

1. 레딧에 회원가입을 합니다. 이 때 아이디와 비밀번호가 꼭 등록되어 있어야 합니다.
2. [레딧 애플리케이션](https://www.reddit.com/prefs/apps)을 생성합니다. **(매우 중요) web app, installed app, script 중 script를 선택합니다.**
3. client id와 client secret 값을 메모합니다.
4. Setup the following secrets for this repo.
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USERNAME`
- `REDDIT_PASSWORD`
5. Add subreddit names in `.github/workflows/slack-reddit-posts.yaml`.

### Slack

1. [슬랙 애플리케이션](https://api.slack.com/apps)을 생성합니다.
2. 슬랙 workspace에 애플리케이션을 설치합니다.
3. In `OAuth & Permissions`, add `chat:write` for `Bot Token Scopes`.
4. Create a new channel and add the application in it.
5. Setup the following secrets for this repo.
- `SLACK_API_TOKEN`
- `SLACK_CHANNEL_ID`


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
               [--slack-api-token SLACK_API_TOKEN]
               [--slack-channel-id SLACK_CHANNEL_ID]

options:
  -h, --help            show this help message and exit
  --reddit-client-id REDDIT_CLIENT_ID               Reddit Client ID
  --reddit-client-secret REDDIT_CLIENT_SECRET       Reddit Client Secret
  --reddit-username REDDIT_USERNAME                 Reddit Username
  --reddit-password REDDIT_PASSWORD                 Reddit Password
  --subreddit-name SUBREDDIT_NAME                   Subreddit Name
  --n-posts N_POSTS                                 Max Posts Number
  --slack-api-token SLACK_API_TOKEN                 Slack API Toekn
  --slack-channel-id SLACK_CHANNEL_ID               Slack Channel ID
```

## Looks like...

<img width="1143" src="https://github.com/Curt-Park/reddit-posts-to-slack/assets/14961526/14315a30-3285-433c-9a2a-5f4387e5814b">

## References

- https://github.com/Curt-Park/reddit-posts-to-slack
- https://velog.io/@iamnotwhale/praw%EB%A1%9C-%EB%A0%88%EB%94%A7-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0
