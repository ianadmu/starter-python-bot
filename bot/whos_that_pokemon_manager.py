import random
import json
import requests
import re

URL =  http://pokeapi.co/api/v2/pokemon/{0}/

class WhosThatPokemonManager(object):
    def __init__:
        self.correct_answer = None
        self.awaiting_answer = False
        self.guessed_correctly_responses = open(os.path.join('./resources', 'pokemon_correct.txt'), 'r')
        self.guessed_incorrectly_responses = open(os.path.join('./resources', 'pokemon_incorrect.txt'), 'r')

    def get_random_pokemon(self):
        num = random.randint(1, 721)
        target = URL.format(num)
        try:
            response = requests.get(target)
        except requests.exceptions.RequestException as e:
            return "Sorry, today is a day of Digimon. No Pokemons for you."
        else:
            pokemon = json.loads(response)
            sprite = pokemon[sprites][front_default]
            self.correct_answer = pokemon['name']
            self.awaiting_answer = True
            return sprite
    
    def check_response(self, user_id, msg):
        if self.awaiting_answer and re.search('it\'?s', msg):
            if re.search(self.cached_correct_response, msg):
                response = reveal_correct_answer + " You go " + user_id + "!"
                return response
            
        elif self.awaiting_answer and re.search('give up|tell|don\'?t know'):
            return self.reveal_correct_answer

    def reveal_correct_answer(self):
        response = "It was " + self.correct_answer
        self.reset_answer
        return response
        
    def reset_answer(self):
        self.correct_answer = None
        self.awaiting_answer = False