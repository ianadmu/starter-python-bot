import random
import os.path
import re


DONT_DELETE = (
    "i came back to life on|winnipeg is currently|loud messages|erased"
)

TEAM_MATES = "nicole|jill|kiera|ian|garrett|malcolm|gurritt|kieratoast"

TESTING_CHANNEL = 'zac-testing'


def is_zac_mention(msg_text):
    return re.search(' ?zac', msg_text.lower())


def is_bot_message(message):
    if 'subtype' in message and message['subtype'] == "bot_message":
        return True
    return False


def should_add_markov(message):
    msg_text = message['text']
    if (
        'attachments' not in message and
        'markov' not in msg_text.lower()
        and not re.search(TEAM_MATES, msg_text.lower())
        and not contains_tag(msg_text)
    ):
        return True
    return False


def should_add_loud(message):
    msg_text = message['text']
    if (
        'user' in message and
        not contains_tag(msg_text) and
        _is_loud(msg_text)
    ):
        return True
    return False


def _is_loud(msg_text):
    emoji_pattern = re.compile(":.*:")

    tokens = msg_text.split()
    if len(tokens) < 2:
        return False
    for token in tokens:
        if not (token.isupper() or emoji_pattern.match(token)):
            return False
    return True


def contains_tag(msg_text):
    user_tag_pattern = re.compile("<@.*")
    channel_tag_pattern = re.compile("<!.*")
    tokens = msg_text.split()
    for token in tokens:
        if user_tag_pattern.match(token) or channel_tag_pattern.match(token):
            return True
    return False


class ResourceManager(object):

    def __init__(self, file_name):
        with open(os.path.join('./resources', file_name), 'r') as f:
            self.responses = f.read().splitlines()

    def get_response(self):
        return random.choice(self.responses)
