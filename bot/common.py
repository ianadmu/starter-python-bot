import random
import os.path


def should_spam():
    random1 = random.random()
    random2 = random.random()
    random3 = random.random()
    if random1 < random2 and random1 < random3:
        return True
    return False


class ResourceManager(object):

    def __init__(self, file_name):
        self.resource_file = open(os.path.join(
            './resources', file_name), 'r'
        )
        self.responses = self.resource_file.readlines()

    def get_response(self):
        return random.choice(self.responses)
