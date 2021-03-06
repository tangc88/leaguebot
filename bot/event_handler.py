import json
import logging
import re

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):

            msg_txt = event['text']

            if self.clients.is_bot_mention(msg_txt) or self._is_direct_message(event['channel']):
                # e.g. user typed: "@pybot tell me a joke!"
                if 'help' in msg_txt:
                    self.msg_writer.write_help_message(event['channel'])
                elif 'trio' in msg_txt:
                    botname, duo, person1, person2, person3 = msg_txt.split(" ")
                    self.msg_writer.write_trio(event['channel'], person1, person2, person3)
                elif '5s' in msg_txt:
                    botname, duo, person1, person2, person3, person4, person5 = msg_txt.split(" ")
                    self.msg_writer.write_5s(event['channel'], person1, person2, person3, person4, person5)
                elif re.search('hi|hey|hello|howdy', msg_txt):
                    self.msg_writer.write_greeting(event['channel'], event['user'])
                elif 'joke' in msg_txt:
                    self.msg_writer.write_joke(event['channel'])
                elif 'duo' in msg_txt:
                    botname, duo, person1, person2 = msg_txt.split(" ")
                    self.msg_writer.write_duo(event['channel'], person1, person2)
                elif 'db' in msg_txt:
                    botname, db, person1, person2 = msg_txt.split(" ")
                    self.msg_writer.write_duo_db(event['channel'], person1, person2)
                elif 'weather' in msg_txt:
                    botname, weather, zip_code = msg_txt.split(" ", 2)
                    self.msg_writer.write_weather(event['channel'], zip_code)
                elif 'leaderboard' in msg_txt:
                    self.msg_writer.write_leaderboard(event['channel'])
                elif 'alternative fact' in msg_txt:
                    self.msg_writer.write_alternative_fact(event['channel'])
                elif 'fact' in msg_txt:
                    self.msg_writer.write_fact(event['channel'])
                elif 'rank' in msg_txt:
                    self.msg_writer.write_rank(event['channel'], event['user'])
                elif 'mastery' in msg_txt:
                    self.msg_writer.write_mastery(event['channel'])
                elif 'attachment' in msg_txt:
                    self.msg_writer.demo_attachment(event['channel'])
                elif 'echo' in msg_txt:
                    self.msg_writer.send_message(event['channel'], msg_txt)
                elif 'duo' in msg_txt:
                    person1 = msg_txt.split(" ", 2)
                    person2 = msg_txt.split(" ", 3)
                    self.msg_writer.write_duo(event['channel'],person1,person2)
                else:
                    self.msg_writer.write_prompt(event['channel'])

    def _is_direct_message(self, channel):
        """Check if channel is a direct message channel

        Args:
            channel (str): Channel in which a message was received
        """
        return channel.startswith('D')
