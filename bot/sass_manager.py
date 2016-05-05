import os.path
import random

class SassManager(object):
	
    def __init__(self):
        self.sass_file = open('sass.txt', 'r').readlines()
        #self.sass_cache = list()
        #self.cache_loaded = False

    def load_sass_cache(self):
        self.sass_cache = self.sass_file.read().splitlines()

    def get_sass(self, msg):
        return self.format_sass(msg)

    def format_sass(self, msg):
        target = self.get_target(msg)
        sass = random.choice(self.sass_file)
        if sass is None:
            sass = " :( "
        return "Hey, " + target+ "! " + sass

    def get_random_sass(self):
        #if not self.cache_loaded:
        #self.load_sass_cache()
        #self.cache_loaded = True
        #self.sass_cache = self.sass_file.read.splitlines()
        return random.choice(self.sass_file)

    def get_target(self, msg):
        token = msg.split("sass ", 1)[1]
        target = self.format_target(token.lower().encode('ascii','ignore'))

    def format_target(self, target):
        if ' me ' in target:
            return "you"
        elif 'yourself' in target:
            return "Zac Efron"
        else:
            return target
