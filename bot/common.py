import random
import os.path


class ResourceManager(object):

    def __init__(self, file_name):
        with open(os.path.join('./resources', file_name), 'r') as f:
            self.responses = f.readlines()

    def get_response(self):
        return random.choice(self.responses)
