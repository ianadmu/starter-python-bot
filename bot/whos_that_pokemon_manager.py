import sys
import random
import json
import requests
import re

URL =  http://pokeapi.co/api/v2/pokemon/{}/

class WhosThatPokemonManager(object):
    def __init__:
        self.correct_answer = None
        self.pos_responses = open(os.path.join('./resources', 'pokemon_correct.txt'), 'r')
        self.neg_responses = open(os.path.join('./resources', 'pokemon_incorrect.txt'), 'r')

    def get_random_pokemon(self):
        num = random.randint(1, 721)
        link = url
        target = link.format(num)
        try:
            response = requests.get(target)
        except requests.exceptions.RequestException as e:
            return "Sorry, today is a day of Digimon. No Pokemons for you."
        else:
            pokemon = json.loads(response)
            sprite = pokemon['sprites']['front_default']
            self.correct_answer = pokemon['name']
            return sprite
    
    def check_response(self, user_id, msg):
        if self.correct_answer is None:
            sys.exit()
        else:
            if re.search(self.correct_answer, msg):
                return self.guessed_correctly(user_id)
            else:
                return user_id + random.choice(self.neg_responses)
            
    def guessed_correctly(self, user_id):
        random_response = random.choice(self.pos_responses)
        revealed_name = self.reveal_answer()
        return random_response + "You go " + user_id + revealed_name + "!"
    
    def gave_up(self):
        if self.correct_answer is None:
            sys.exit()
        else:
            return self.reveal_answer()   
                
    def reveal_answer(self):
        answer = self.correct_answer
        self.correct_answer = None
        return " It was " + self.correct_answer