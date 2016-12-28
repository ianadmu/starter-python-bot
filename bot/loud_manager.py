import logging
import random
import os.path
from persistance_manager import PersistanceManager 

class LoudManager(object):
    def __init__(self):
    	self.a = 2
        self.persistance_manager  = PersistanceManager("/louds.txt", seed_file="./resources/seed_louds.txt")

    def write_loud_to_file(self, loudMessage):
        loudMessage = loudMessage.encode("utf8")
        self.persistance_manager.append_to_data(loudMessage.replace("\n", " ")+"\n")


    def get_random_loud(self):
        louds = self.persistance_manager.get_data().split("\n")
        if louds == None:
        	return ""

        return random.choice(louds)