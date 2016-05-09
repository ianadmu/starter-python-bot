import os.path
import random
import re

class ApologyManager(object):

    def __init__(self):
        self.apology_file = open(os.path.join('./resources', 'apologies.txt'), 'r')
        self.apologies = self.apologies.readlines()

    def get_random_apology(self):
        return random.choice(self.apologies)
