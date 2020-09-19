from flask import abort, Flask, jsonify, request
from slackeventsapi import SlackEventAdapter
import os

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], "/slack/events", app)
@slack_events_adapter.on("message")
def hookSlackEvents(event_data):
        app.logger.debug(event_data)
