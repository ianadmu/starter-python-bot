import os.path
import random
import re

sass_flag = re.compile('sass[a-z]* ')

class SassManager(object):
	
    def __init__(self):
        self.sass_file = open(os.path.join('./resources', 'sass.txt'), 'r')
        self.sass_cache = self.sass_file.readlines()

    def get_sass(self, msg):
        return self.format_sass(msg)

    def format_sass(self, msg):
        target = self.get_target(msg)
        sass = random.choice(self.sass_cache)
        return 'Hey, {}! {}'.format(target, sass)

    def get_target(self, msg):
        token = re.split(sass_flag, msg)
        target = self.format_target(token[1]) #token[1].lower().encode('ascii','ignore')
        return target

    def format_target(self, target):
        if 'me' in target:
            return "you"
        elif 'yourself' in target:
            return "Zac Efron"
        elif target.startswith('@'):
            return '<{}>'.format(target)
        else:
            return target.title()
