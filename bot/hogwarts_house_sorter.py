import random

HOUSES = ['Gryffindor','Ravenclaw','Slytherin','Hufflepuff']

class HogwartsHouseSorter(object):
	def get_random_house(self):
		return random.choice(HOUSES)


