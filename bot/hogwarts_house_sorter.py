import random
import xml.etree.ElementTree as ET   

HOUSES = ['GRYFFINDOR','RAVENCLAW','SLYTHERIN','HUFFLEPUFF']

class HogwartsHouseSorter(object):
	def get_house_description(self, house):
		tree = ET.parse('house_descriptions.xml')
		root = tree.getroot()
		random_Number = int(random.random()*6) #num of descriptions in the xml file
		return root[HOUSES.index(house)][random_Number].text

	def get_random_house(self):
		house = random.choice(HOUSES)		
		description = self.get_house_description(house)
		return "You have been sorted into: " + house + "!\n" + description
