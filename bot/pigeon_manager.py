class Pigeon(object):

    def __init__(self):
    	self.pigeon_noises = ["Coo","Coo","Coo","Coo","Coo","Coo", "Coo coo","Caw Caw","Chirp",
            "CooOOoooOO", "Cee Chee Cee", "Caw", "Ouip Ouip", "Chika dee", "Chika dee dee dee", "CaCAAA",
            "C-c-c-c-c-caaaaaaa~!", "Tweet", "Coocoocachoo", "Cookle doodle doo","Coo","Coo","Coo","Coo",
            "Coo cooooOOOO cooo coo ca coooo coo", "Tweeeet", "Ca-CAWWWWWWWWW","Coo","Coo", "Coo coo","Caw Caw","Chirp",
            "CooOOoooOO", "Cee Chee Cee", "Caw", "Ouip Ouip", "Chika dee", "Chika dee dee dee", "CaCAAA",
            "Coo", "Caaaaw ca ca caaaa", "Coocoocachoo", "Coodle doodle doo","Coo","Coo","Coo","Coo","Coo",
            "Tweet", "Tweeeet", "Ca-CAWWWWWWWWW","Coo","Coo", "Coo coo","Caw Caw","Chirp","Coo","Coo","Coo",
            "CooOOoooOO", "Cee Chee Cee", "Caw", "Ouip Ouip", "Chika dee", "Chika dee dee dee", "CaCAAA",
            "Coo - Coo Ca Chaa", "Caaaaw ca ca caaaa", "Coocoocachoo", "Coodle doodle doo","Coo","Coo","Coo",
            "Coo cooooOOOO cooo coo ca coooo coo", "Tweeeet", "cluck cluck cluck cluck cluck cluck cluckAAAAAAAW!", "I'm really a dove, you know",
            "I'm going to grow up to be a swan", "*Insert bird noises here", "*flaps wings", "*pecks ground",
            "* nibbles at neck", "* eats worm", "*twitches","Coo Coo *Cough Coo","Coo","Coo","Coo","Coo","Coo","Coo",
            "Coo","Coo","Coo","Coo","Coo","Coo","Coo","Coo","Coo","Coo","Coo","Coo","Coo","Coo","Coo",
            "Brerererer","Brerererer","Brerererer","Brerererer","Brerererer","Brerererer","Brerererer"]

    def pigeonate(self, text):
    	hashValue = 11;
    	for character in text:
    		hashValue *= 47
    		hashValue += ord(character)
        return self.pigeon_noises[hashValue % len(self.pigeon_noises)]
