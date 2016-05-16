import json
import requests
import re

pkmn_flag = re.compile(' (I|i) choose you')
URL =  'http://pokeapi.co/api/v2/pokemon/{}/'

class PokemonCaster(object):
                 
    def i_choose_you(self, msg):
        token = re.split(pkmn_flag, msg)
        link = URL
        target = link.format(token[0])
        try:
            response = requests.get(target)
        except requests.exceptions.RequestException as e:
            return None
        else:
            pokemon = response.json()
            return pokemon['sprites']['front_default']