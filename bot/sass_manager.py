import re
from markov import Markov

sass_flag = re.compile('sass[a-z]* ')


class SassManager(object):

    def __init__(self):
        self.sassMarkov = Markov(3)
        self.sassMarkov.add_file('insults.txt')

    def get_sass(self, msg):
        target = self.get_target(msg)
        sass = str(self.sassMarkov)
        return 'Hey, {}! {}'.format(target, sass)

    def get_target(self, msg):
        token = re.split(sass_flag, msg.lower())
        target = self.format_target(token[1])
        return target

    def format_target(self, target):
        if target == 'me':
            return 'you'
        elif target == 'yourself':
            return 'Zac Efron'
        elif '<@' in target:
            return target.upper()
        else:
            return target.title()
