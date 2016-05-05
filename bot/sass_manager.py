import os.path
import random

class SassManager(object):
	
    def __init__(self):
        self.sass_file = open('sass.txt', 'r')
        self.sass_cache = self.sass_file.readlines()
        #self.cache_loaded = False

    def get_sass(self, msg):
        return self.format_sass(msg)

    def format_sass(self, msg):
        target = self.get_target(msg)
        sass = random.choice(self.sass_cache)
        return "Hey, " + target+ "! " + sass

    def get_target(self, msg):
        token = msg.split("sass ", 1)[1]
        target = self.format_target(token.lower().encode('ascii','ignore'))
        return target

    def format_target(self, target):
        if 'me ' in target:
            return "you"
        elif 'yourself' in target:
            return "Zac Efron"
        else:
            return target
