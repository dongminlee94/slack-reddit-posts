"""Notifier for sending messages to Slack channels and threads."""

from slack_sdk import WebClient


class SlackNotifier:
    """Handler for sending Slack messages using the WebClient."""

    def __init__(self, token: str) -> None:
        """Initialize the Slack client with an API token."""
        self._client = WebClient(token=token)

    def send_main_message(self, channel_id: str, text: str) -> str:
        """Send a message to a specified Slack channel."""
        response = self._client.chat_postMessage(channel=channel_id, text=text)

        return response["ts"]  # pyrefly: ignore

    def send_thread_message(self, channel_id: str, text: str, thread_ts: str) -> None:
        """Send a reply message within a specific Slack thread."""
        self._client.chat_postMessage(channel=channel_id, text=text, thread_ts=thread_ts)
