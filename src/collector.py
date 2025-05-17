"""Reddit post and comment collector using PRAW."""

from collections import deque

import praw
from praw.models.reddit.submission import Submission


class RedditCollector:
    """Handler for Reddit API interactions to collect posts and comments."""

    def __init__(self, client_id: str, client_secret: str, username: str, password: str) -> None:
        """Initialize the Reddit client with provided credentials."""
        self._reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=f"script by /u/{username}",
            username=username,
            password=password,
        )

    def _get_all_comments_text(self, submission: Submission) -> str:
        """Retrieve and formats all comments and replies for a given submission."""
        all_comments_text = []

        submission.comments.replace_more(limit=None)
        comment_queue = deque(submission.comments)  # type: ignore

        while comment_queue:
            comment = comment_queue.popleft()
            author = comment.author.name if comment.author else "[deleted]"
            indent = "\t" * comment.depth
            all_comments_text.append(
                f"{indent}- [{author}, Score: {comment.score}] {comment.body.replace(chr(10), ' ')}"
            )
            comment_queue.extend(comment.replies)

        return "\n".join(all_comments_text)

    def collect_hot_posts(self, subreddit_name: str, n_posts: int) -> list[dict[str, str]]:
        """Collect top 'hot' posts, their text, and comments from a subreddit."""
        subreddit = self._reddit.subreddit(subreddit_name)

        submissions_data = []

        for submission in subreddit.hot(limit=n_posts):
            if submission.stickied:
                continue

            title = f"<{submission.url}|{submission.title}> [Upvotes {submission.score}]"
            selftext = submission.selftext
            comments_text = self._get_all_comments_text(submission)
            contents = f"제목:\n{title}\n\n본문:\n{selftext}\n\n댓글:\n{comments_text}"

            submissions_data.append({"title": title, "contents": contents})

        return submissions_data
