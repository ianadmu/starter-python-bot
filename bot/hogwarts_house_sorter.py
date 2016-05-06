import random
import xml.etree.ElementTree as ET   

HOUSES = ['GRYFFINDOR','RAVENCLAW','SLYTHERIN','HUFFLEPUFF']

class HogwartsHouseSorter(object):

	def get_house(self, msg):
		msg = msg.upper();
		index = int(random.random()*4)
		for num in range(4):
			if HOUSES[index] in msg.upper():
				return HOUSES[index]
			else:
				index = (index+1)%4
		return random.choice(HOUSES)

	def get_house_description(self, house):
		tree = ET.parse('house_descriptions.xml')
		root = tree.getroot()
		random_Number = int(random.random()*6) #min num of descriptions in the xml file per house
		return root[HOUSES.index(house)][random_Number].text

	def sort_into_house(self, msg):
		house = self.get_house(msg)	
		description = self.get_house_description(house)
		return "You have been sorted into: " + house + "!\n" + description

