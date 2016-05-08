
import logging
import re
import time
import json

from slacker import Slacker
from slackclient import SlackClient

logger = logging.getLogger(__name__)


class SlackClients(object):
    def __init__(self, token):
        self.token = token

        # Slacker is a Slack Web API Client
        self.web = Slacker(token)

        # SlackClient is a Slack Websocket RTM API Client
        self.rtm = SlackClient(token)

    def bot_user_id(self):
        return self.rtm.server.login_data['self']['id']

    def is_message_from_me(self, user):
        return user == self.rtm.server.login_data['self']['id']

    def is_bot_mention(self, message):
        bot_user_name = self.rtm.server.login_data['self']['id']
        if re.search("@{}".format(bot_user_name), message):
            return True
        else:
            return False

    def send_user_typing_pause(self, channel_id, sleep_time=3.0):
        user_typing_json = {"type": "typing", "channel": channel_id}
        self.rtm.server.send_to_websocket(user_typing_json)
        time.sleep(sleep_time)

    def send_time_triggered_msg(self, channel_name, msg):
    	self.rtm.api_call('chat.postMessage', as_user='true:', channel=channel_name, text=msg)

    def byteify(input):
    	if isinstance(input, dict):
        	return {byteify(key): byteify(value)
        			for key, value in input.iteritems()}
    	elif isinstance(input, list):
        	return [byteify(element) for element in input]
    	elif isinstance(input, unicode):
        	return input.encode('utf-8')
    	else:
        	return input

    def get_random_emoji(self):
    	response = self.rtm.api_call('emoji.list')
    	emojis = response['emoji'].items()
    	    	#return int(random.random()*58
    	return emojis[0][0]