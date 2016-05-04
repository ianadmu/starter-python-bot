import random

HOUSES = ['GRYFFINDOR','RAVENCLAW','SlYTHERIN','HUFFLEPUFF']
HUFFLEPUFF = ["Hufflepuffs are defined by their love of family, comfort, and living things first and foremost. Anything involving animals or plants is going to appeal to them: Care of Magical Creatures and Herbology are subjects beloved by Hufflepuffs. They also care deeply for people and enjoy the company of others; being alone or feeling unloved are things Puffs dislike intensely. ",
				"Hufflepuffs are interested in helping both people and animals, but are much less confrontational or daring than Gryffindors. They’re the least likely to care about individual achievement or House points, and most likely to focus on their relationships to others rather than things they personally have done."]
RAVENCLAW = ["Hufflepuffs are defined by their love of family, comfort, and living things first and foremost. Anything involving animals or plants is going to appeal to them: Care of Magical Creatures and Herbology are subjects beloved by Hufflepuffs. They also care deeply for people and enjoy the company of others; being alone or feeling unloved are things Puffs dislike intensely. ",
				"Hufflepuffs are interested in helping both people and animals, but are much less confrontational or daring than Gryffindors. They’re the least likely to care about individual achievement or House points, and most likely to focus on their relationships to others rather than things they personally have done."]
SLYTHERIN = ["Hufflepuffs are defined by their love of family, comfort, and living things first and foremost. Anything involving animals or plants is going to appeal to them: Care of Magical Creatures and Herbology are subjects beloved by Hufflepuffs. They also care deeply for people and enjoy the company of others; being alone or feeling unloved are things Puffs dislike intensely. ",
				"Hufflepuffs are interested in helping both people and animals, but are much less confrontational or daring than Gryffindors. They’re the least likely to care about individual achievement or House points, and most likely to focus on their relationships to others rather than things they personally have done."]
GRYFFINDOR = ["Hufflepuffs are defined by their love of family, comfort, and living things first and foremost. Anything involving animals or plants is going to appeal to them: Care of Magical Creatures and Herbology are subjects beloved by Hufflepuffs. They also care deeply for people and enjoy the company of others; being alone or feeling unloved are things Puffs dislike intensely. ",
				"Hufflepuffs are interested in helping both people and animals, but are much less confrontational or daring than Gryffindors. They’re the least likely to care about individual achievement or House points, and most likely to focus on their relationships to others rather than things they personally have done."]
class HogwartsHouseSorter(object):
	def get_random_house(self):
		house = random.choice(HOUSES)
		return "You have been sorted into: " + house + "!\n" + random.choice(house)

