import random
import os.path
import re


DONT_DELETE = 'i came back to life on|winnipeg is currently|added|erased'


def contains_user_tag(message):
    tag_pattern = re.compile("<@.*")
    tokens = message.split()
    for token in tokens:
        if tag_pattern.match(token):
            return True
    return False


class ResourceManager(object):

    def __init__(self, file_name):
        with open(os.path.join('./resources', file_name), 'r') as f:
            self.responses = f.readlines()

    def get_response(self):
        return random.choice(self.responses)
