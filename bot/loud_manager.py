# this is for when persistance works
# import logging
# import random
# import os.path
# from persistance_manager import PersistanceManager

# class LoudManager(object):
#     def __init__(self):
#     	self.a = 2
#         self.persistance_manager  = PersistanceManager(
#              "/louds.txt", seed_file="./resources/seed_louds.txt"
#         )

#     def write_loud_to_file(self, loudMessage):
#         loudMessage = loudMessage.encode("utf8")
#         self.persistance_manager.append_to_data(
#             loudMessage.replace("\n", " ")+"\n"
#         )


#     def get_random_loud(self):
#         louds = self.persistance_manager.get_data()

#         if louds == None:
#         	return ""
#         else:
#             louds = louds.split("\n")
#         return random.choice(louds)

import random
import os.path


class LoudManager(object):
    def __init__(self):
        self.loud_file = open(
            os.path.join('./resources', 'seed_louds.txt'), 'a+'
        )
        self.loud_cache = list()
        self.cache_loaded = False

    def write_loud_to_file(self, loudMessage):
        loudMessage = loudMessage.encode("utf8").replace("\n", " ")
        if loudMessage not in self.loud_cache:
            self.loud_file.write(loudMessage + "\n")
            self.loud_cache.append(loudMessage)

    def load_loud_cache(self):
        self.loud_cache = list(self.loud_file.readlines())

    def get_random_loud(self):
        if not self.cache_loaded:
            self.load_loud_cache()
            self.cache_loaded = True
        return random.choice(self.loud_cache)
