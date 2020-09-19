import os
import sys

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], "/slack/events", app)

slack_bot_token = os.environ["SLACK_OAUTH_TOKEN"]
slack_client = WebClient(slack_bot_token)


@slack_events_adapter.on("message")
def handle_message_greeting(event_data):
    print("debug:handled function: {}".format(sys._getframe().f_code.co_name))
    print("debug:eventdata:{}".format(event_data))
    message = event_data["event"]
    if message.get("subtype") is None and message.get("bot_id") is None:
        channel = message["channel"]
        res_message = message.get("text") + ":dolphin:"
        slack_client.chat_postMessage(channel=channel, text=res_message)
