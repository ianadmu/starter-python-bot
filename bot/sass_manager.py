import os.path
import random
import re

sass_flag = re.compile('sass[a-z]* ')

class SassManager(object):
	
    def __init__(self):
        self.sass_file = open(os.path.join('./resources', 'sass.txt'), 'r')
        self.sass_cache = self.sass_file.readlines()

    def get_sass(self, user_id, msg):
        return self.format_sass(user_id, msg)

    def format_sass(self, user_id, msg):
        target = self.get_target(user_id, msg)
        sass = random.choice(self.sass_cache)
        return 'Hey, <@{}>! {}'.format(user_id, sass)

    def get_target(self, user_id, msg):
        token = re.split(sass_flag, msg)
        target = self.format_target(token[1].lower().encode('ascii','ignore'), user_id)
        return target

    def format_target(self, target, user_id):
        if 'me' in target:
            return "you"
        elif 'yourself' in target:
            return "Zac Efron"
        elif target.startswith('@'):
            return '<@{}>'.format(user_id)
        else:
            return target.title()
