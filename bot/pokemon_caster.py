import json
import requests
import re

URL =  'http://pokeapi.co/api/v2/pokemon/{}/'

teammates = { kiera, nicole, jill, malcolm, ian}

class PokemonCaster(object):
                 
    def i_choose_you(self, msg):
        token = msg.split()
        link = URL
        target = link.format(token[0])
        try:
            response = requests.get(target)
        except requests.exceptions.RequestException as e:
            return None
        else:
            pokemon = response.json()
            if 'sprites' in pokemon:
                return pokemon['sprites']['front_default']
             elif msg in teammates:
                return :msg:
                