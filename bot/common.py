import random

channels = {
    'slackers': {
        'zac-testing': 'C1SDALDG9'

    },
    'iq': {
        'zac-testing': 'C171ASJJK'
    }
}


def should_spam():
    random1 = random.random()
    random2 = random.random()
    random3 = random.random()
    if random1 < random2 and random1 < random3:
        return True
    return False
