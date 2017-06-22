import random
import os.path
import re


DONT_DELETE = (
    "i came back to life on|winnipeg is currently|loud messages|erased|news: "
)

TEAM_MATES = "nicole|jill|kiera|ian|garrett|malcolm|gurritt|kieratoast"

USER_TAG = re.compile("<@.*")
CHANNEL_TAG = re.compile("<!.*")

TESTING_CHANNEL = 'zac-testing'


def is_zac_mention(msg_text):
    return re.search(' ?zac', msg_text.lower())


def is_bot_message(message):
    if 'subtype' in message and message['subtype'] == "bot_message":
        return True
    return False


def should_add_markov(message):
    user_id = message['user'] if 'user' in message else None
    msg_text = message['text']
    if is_bot_message(message) or user_id == "U1LA33VC4":
        return False
    if (
        'attachments' not in message
        and not re.search('markov|zac', msg_text.lower())
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


def contains_tag(msg_text):
    tokens = msg_text.split()
    for token in tokens:
        if USER_TAG.match(token) or CHANNEL_TAG.match(token):
            return True
    return False


def get_target(flag, msg_txt):
    token = re.split(flag, msg_txt.lower())
    target = ""
    if len(token) > 1:
        target = _format_target(token[1])
    return target


class ResourceManager(object):

    def __init__(self, file_name):
        with open(os.path.join('./resources', file_name), 'r') as f:
            self.responses = f.read().splitlines()

    def get_response(self):
        return random.choice(self.responses)

    def get_all(self):
        return ' \n'.join(line for line in self.responses)

    def get_count(self):
        return len(self.responses)


"""Methods that should only be used from this file"""


def _is_loud(msg_text):
    emoji_pattern = re.compile(":.*:")

    tokens = msg_text.split()
    if len(tokens) < 2:
        return False
    for token in tokens:
        if not (token.isupper() or emoji_pattern.match(token)):
            return False
    return True


def _format_target(target):
    if target == 'me':
        return 'you'
    elif target == 'yourself' or is_zac_mention(target):
        return 'Zac Efron'
    elif '<@' in target:
        return target.upper()
    else:
        return target.title()
