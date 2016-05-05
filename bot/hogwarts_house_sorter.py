import random

HOUSES = ['GRYFFINDOR','RAVENCLAW','SlYTHERIN','HUFFLEPUFF']
HUFFLEPUFF = ['1','2','3']
RAVENCLAW = ['1','2','3']
SLYTHERIN = ['1','2','3']
GRYFFINDOR = ['1','2','3']

class HogwartsHouseSorter(object):
	def get_house_description(house):
		if house == 'GRYFFINDOR':
			return random.choice(GRYFFINDOR)
		elif house == 'RAVENCLAW':
			return random.choice(RAVENCLAW)
		elif house == 'SLYTHERIN':
			return random.choice(SlYTHERIN)
		else:
			return random.choice(HUFFLEPUFF)

	def get_random_house(self):
		house = random.choice(HOUSES)
		description = HogwartsHouseSorter.get_house_description(house)
		return "You have been sorted into: " + house + "!\n" + description

