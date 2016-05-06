import os.path
import random
import re

class ApologyManager(object):
    
    def __init__(self)
        self.apologies = open(os.path.join('./resources', 'apologies.txt'), 'r')
        self.apology_cache = self.apologies.readlines()
    
    def get_random_apology(self):
        return random.choice(self.apology_cache)