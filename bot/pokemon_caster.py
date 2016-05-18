import json
import requests
import re

URL =  'http://pokeapi.co/api/v2/pokemon/{}/'

class PokemonCaster(object):
                 
    def i_choose_you(self, msg):
        token = msg.split()
        link = URL
        target = link.format(token[0].lower())
        try:
            response = requests.get(target)
        except requests.exceptions.RequestException as e:
            return None
        else:
            pokemon = response.json()
            if 'sprites' in pokemon:
                return pokemon['sprites']['front_default']