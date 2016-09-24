# coding=utf-8

import logging
import random
import re
import os.path
import xkcd_manager
import weather_manager
import common
import traceback

from loud_manager import LoudManager
from whos_that_pokemon_manager import WhosThatPokemonManager
from pokemon_caster import PokemonCaster
from hogwarts_house_sorter import HogwartsHouseSorter
from sass_manager import SassManager
from food_getter import FoodGetter
from apology_manager import ApologyManager
from equation_manager import EquationManager
from channel_manager import ChannelManager

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.loud_manager = LoudManager()
        self.whos_that_pokemon_manager = WhosThatPokemonManager()
        self.pokemon_caster = PokemonCaster()
        self.hogwarts_house_sorter = HogwartsHouseSorter()
        self.sass_manager = SassManager()
        self.apology_manager = ApologyManager()
        self.food_getter = FoodGetter()
        self.explanation_manager = ResourceManager('explanations.txt')
        self.equation_manager = EquationManager()
        self.channel_manager = ChannelManager(self.clients)

    def __del__(self):
        closing_msgs = ["No!! Don't kill me! I want to live!", "Good BYEEE!!!",
                        "I'm dying again :sob:",
                        "Have you gotten tired of this face :zacefron: ?"]
        txt = random.choice(closing_msgs)
        self.send_message('zac-testing', txt)

    def __exit__(self, exception_type, exception_value, traceback):
        self.send_message('zac-testing', 'exit')

    def send_message_as_other(self, channel_id, msg, username, emoji):
        channel_id = self.channel_manager.get_channel_id(channel_id)
        msg = msg.replace('&', "&amp;")
        # msg = msg.replace('<', "&lt;")
        # msg = msg.replace('>', "&gt;")
        # msg = msg.decode("utf8", "ignore")

        self.clients.send_message_as_other(channel_id, msg, username, emoji)

    def send_message(self, channel_id, msg):
        channel_id = self.channel_manager.get_channel_id(channel_id)
        msg = msg.replace('&', "&amp;")
        # msg = msg.replace('<', "&lt;")
        # msg = msg.replace('>', "&gt;")
        # msg = msg.decode("utf8", "ignore")

        self.clients.send_message(channel_id, msg)

    def send_attachment(self, channel_id, txt, attachment):
        try:
            result = self.clients.send_attachment(channel_id, txt, attachment)
            if "ok" not in result:
                raise Exception
        except Exception as e:
            self.write_custom_error(str(e))
        except:
            err_msg = traceback.format_exc()
            logging.error('Unexpected error: {}'.format(err_msg))
            self.write_error('zac-testing', err_msg)
            pass

    def write_channel_id(self, channel_id):
        self.send_message(
            'zac-testing', self.channel_manager.get_channel_id(channel_id)
        )

    def write_custom_error(self, msg):
        self.send_message('zac-testing', msg)

    def write_error(self, channel_id, err_msg):
        txt = (":face_with_head_bandage: my maker didn't handle this error "
               "very well:\n>```{}```").format(err_msg)
        self.send_message(channel_id, txt)

    def write_slow(self, channel_id, msg):
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, msg)

    def send_reaction(self, emoji_name, channel_id, timestamp):
        self.clients.send_reaction(emoji_name, channel_id, timestamp)

    def write_closing(self):
        self.send_message('zac-testing', "I'm closing, ~byeeee~!!!!!")

    def write_message_deleted(self, channel_id):
        txt = ("I SAW THAT! _Someone_ deleted a message from channel: "
               "<#{}>").format(channel_id)
        self.send_message('zac-testing', txt)

    def write_left_channel(self, channel_id):
        txt = '...well THAT was something'
        self.send_message(channel_id, txt)

    def write_joined_channel(self, channel_id, user_id):
        if (common.channels['iq']['zac-testing'] or
                channel_id == common.channels['slackers']['zac-testing']):
            txt = ("Hey <@{}>! Welcome to the Testing (aka the Weather) "
                   "channel. Please MUTE this channel or be inundaded with "
                   "notifications!").format(user_id)
            self.write_slow(channel_id, txt)
            self.write_xkcd(channel_id, "15")
        else:
            self.write_greeting(channel_id, user_id)

    def write_help_message(self, channel_id):
        help_txt = [
            "_Hint: sometimes you need to say my name for me to respond!_",
            "> `Hi` - I'll greet back, i don't bite. :wave:",
            "> `Joke` - I'll tell you one of my finest jokes :laughing:",
            "> `Weather` - Let me tell you the weather in Winnipeg. :rainbow:",
            "> `I'm sad` - Maybe I can cheer you up. :wink:",
            "> `Sort me` - I'll sort you into a Hogwarts house!",
            ("> `Apologize` - Sometimes I make mistakes. Tell me when I do so "
                "I can apologize. :bow:"),
            "> `Thanks!` - I also like to be appreciated :innocent:",
            "> `Solve <equation>` - Math sucks. I can help! :nerd_face:",
            ("> `Sass <name>` - I'll be sure to sass <name> until the sun "
                "burns out. :smiling_imp:"),
            ">`Riri` - WORK WORK WORK WORK WORK",
            ("> `Good morning` - I shall wish you a very good morning as "
                "well! :sunny:"),
            "> `Good night` - I'll say good night! :crescent_moon:",
            "> `Who's that pokemon?` - Are you a pokemon master? :slowpoke:",
            "> `Explain | Why` - I'll explain what's going on :reginageorge:",
            ("> `French <phrase>` - I know flawless French! I'll translate "
                "for you :bombardier:"),
            "> `Marry me` - ...Are you going to propose to me?? _Le gasp_ ",
            "> `I love you` - ...Do you really!? :heart:",
            "> `Sweetpotato me` - Sometimes you just need a :sweet_potato:",
            "> `Boyer` - I'll give you one of boyer's wise quotes :nerd_face:",
            "> `:joy:` - Sometimes it's hard for me to control my laughter!",
            ("> `Wiener` - You wanna know who is a wiener? I'll tell you "
                ":eggplant:"),
            "> `Draw me` - I am _le best artist_ :art:",
            ("> `<pokemon> I choose you!` - Are you going to be the very "
                "best? :yourturn:"),
            "> `Encourage me` - Let me help you get back on track. :grinning:",
            "> `Feed me` - Have some food courtesy of moi :banana:",
            "> `Fuck this` - Don't worry I got just the video. :+1:",
            "> `Just Do it` - Need some motivation? :just_do_it:",
            "> `Markov` - I like to mix things up a bit too :lips:",
            "> `Coo` - Want a pigeon sound? Pigeon Mode is for you! :parrot:",
            ("> `XKCD` - Want an XKCD comic? Type it's number, or get the "
                "latest one"),
            "> `TicTacToe` - Want to play TicTacToe? See also `TicTacToe help`"
        ]
        txt = ("I'm Zac Efron.  I'll *_respond_* to the following {0} "
               "commands:\n").format(len(help_txt)-1)
        for val in range(len(help_txt)):
            txt += help_txt[val]
            txt += '\n'

        self.write_slow(channel_id, txt)

    def write_to_french(self, channel_id, msg):
        msg = msg.lower()
        msg = msg.replace('zac', '')
        msg = msg.replace('french', '')
        tokens = msg.split()
        response = ' '.join(tokens)
        txt = '_le {}_'.format(response)
        self.write_slow(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.write_slow(channel_id, txt)

    def write_good_night(self, channel_id, user_id):
        nights = [
            'Goodnight', ':crescent_moon: Good night',
            'Goodnight, my dear', 'Sweet dreams',
            'Don\'t let the bed bugs bite', 'Pleasant dreams',
            'Sleep well', 'Until tomorrow then',
            'May your dreams be filled with my beautiful face :zacefron:'
        ]
        txt = '{}, <@{}>!'.format(random.choice(nights), user_id)
        self.write_slow(channel_id, txt)

    def write_spelling_mistake(self, channel_id, timestamp):
        emoji_name = "spelft_it_wronbg_again_i_see"
        self.send_reaction(emoji_name, channel_id, timestamp)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = ("I'm sorry, I didn't quite understand... Can I help you? "
               "(e.g. `<@" + bot_uid + "> help`)")
        self.write_slow(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.write_slow(channel_id, question)
        answer = "To eat the chicken on the other side! :laughing:"
        self.write_slow(channel_id, answer)

    def write_encouragement(self, channel_id, user_id):
        txt = 'Get your shit together <@{0}>'.format(user_id)
        self.write_slow(channel_id, txt)

    def write_food(self, channel_id):
        food = self.food_getter.get_random_food()
        self.write_slow(channel_id, food)

    def write_bang(self, channel_id, user_id):
        bang = 'BANG you\'re dead <@{}> :gun:'.format(user_id)
        self.write_slow(channel_id, bang)

    def write_cast_pokemon(self, channel_id, msg):
        pkmn = self.pokemon_caster.i_choose_you(msg)
        if pkmn is not None:
            self.send_message(channel_id, pkmn)

    def write_whos_that_pokemon(self, channel_id):
        txt = self.whos_that_pokemon_manager.whos_that_pkmn()
        self.send_message(channel_id, txt)

    def write_pokemon_guessed_response(self, channel_id, user_id, msg):
        result = self.whos_that_pokemon_manager.check_response(user_id, msg)
        if result is not None:
            self.send_message(channel_id, result)

    def write_sad(self, channel_id):
        txt = "This always cracks me up. :wink:"
        self.write_slow(channel_id, txt)
        attachment = {
            "title": "/giphy bloopin",
            "title_link": ("http://giphy.com/gifs/friday-rebecca-black-hurrr-"
                           "13FsSYo3fzfT2g"),
            "image_url": "http://i.giphy.com/13FsSYo3fzfT2g.gif",
            "color": "#7CD197",
        }
        self.send_attachment(channel_id, "", attachment)
        txt = "I'm crying into my tea. :joy:"
        self.write_slow(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = ("Beep Beep Boop is a ridiculously simple hosting platform for "
               "your Slackbots.")
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": ("https://storage.googleapis.com/beepboophq/_assets/"
                          "bot-1.22f6fb.png"),
            "color": "#7CD197",
        }
        self.send_attachment(channel_id, txt, attachment)

    def write_weather(self, channel_id):
        # line1 = WeatherController.get_weather()
        # line1 = "Sorry, I don't know the weather today :zacefron: "
        # line2 = "Anyways, it's always hot when I'm around :sunglasses: "
        response = weather_manager.getCurrentWeather()
        self.write_slow(channel_id, response)

    def write_loud(self, channel_id, orig_msg):
        zac_mentioned = re.search(' ?zac', orig_msg.lower())
        if not zac_mentioned:
            self.loud_manager.write_loud_to_file(orig_msg)
        if zac_mentioned or common.should_spam():
            self.send_message(channel_id, self.loud_manager.get_random_loud())

    def write_hogwarts_house(self, channel_id, user_id, msg):
        response = self.hogwarts_house_sorter.sort_into_house(msg)
        txt = '<@{}>: {}'.format(user_id, response)
        self.write_slow(channel_id, txt)

    def write_explanation(self, channel_id):
        self.write_slow(channel_id, self.explanation_manager.get_explanation())

    def write_sass(self, channel_id, msg):
        txt = self.sass_manager.get_sass(msg)
        self.write_slow(channel_id, txt)

    def write_apology(self, channel_id):
        txt = self.apology_manager.get_random_apology()
        self.write_slow(channel_id, txt)

    def write_solution(self, channel_id, msg):
        self.write_slow(channel_id, self.equation_manager.solve(msg))

    def write_sweetpotato_me(self, channel_id, user_id):
        txt = 'Here, <@{}>! :sweet_potato:'.format(user_id)
        self.write_slow(channel_id, txt)

    def write_marry_me(self, channel_id):
        responses = [
            'OKAY! :ring:', 'Ummm, how \'bout no.',
            'Shoot I would...if you were :kiera:', '_le shrug_ \'k.',
            'R-Really? Okay, I shall be your ~bride~ husband from now on!!',
            'Sorry but I\'m already married to my job.',
            'Sorry, but I\'m already married to :nicole:',
            'HOW DO I KNOW YOU WON\'T CHEAT ON ME WITH QBOT?!??',
            '_le HELLS YES!_',
            ('Sorry, but you are human, and I am a mere bot. It could never '
                'work out between us...'),
            (':musical_note: _IF YOU LIKE IT THEN YOU SHOULDA PUT A RING ON '
                'IT_:musical_note:'), 'No. Never. Nope. Nu-uh.'
        ]
        txt = '{}'.format(random.choice(responses))
        self.write_slow(channel_id, txt)

    def write_draw_me(self, channel_id):
        file = open(os.path.join('./resources', 'draw_me.txt'), 'r')
        urls = file.read().splitlines()
        txt = '{}'.format(random.choice(urls))
        self.write_slow(channel_id, txt)

    def write_forever(self, channel_id):
        file = open(os.path.join('./resources', 'forever.txt'), 'r')
        comments = file.read().splitlines()
        txt = '{}'.format(random.choice(comments))
        self.write_slow(channel_id, txt)
        answer = '{}'.format('Just kidding! :laughing:')
        self.write_slow(channel_id, answer)
        emoji = ':{}:'.format('trollface')
        self.write_slow(channel_id, emoji)

    def write_flip(self, channel_id):
        self.send_message(channel_id, u"(╯°□°）╯︵ ┻━┻")

    def write_unflip(self, channel_id):
        self.send_message(channel_id, u"┬─┬ノ( º _ ºノ)")

    def write_sup_son(self, channel_id):
        self.send_message(channel_id, u"¯\_(ツ)_/¯")

    def write_riri_me(self, channel_id, msg):
        riri_flag = re.compile('riri[a-z]* ')
        token = re.split(riri_flag, msg.lower())
        if len(token) > 1:
            target = token[1]
            target = target.upper()
        else:
            target = "WHY WOULD YOU JUST TYPE RIRI?\n"
        txt = ' '.join(target for num in range(5))
        self.write_slow(channel_id, txt)

    def write_xkcd(self, channel_id, msg):
        txt = xkcd_manager.getImageLocation(msg)
        self.write_slow(channel_id, txt)


class ResourceManager(object):

    def __init__(self, file_name):
        self.resource_file = open(os.path.join(
            './resources', file_name), 'r'
        )
        self.responses = self.resource_file.readlines()

    def get_random_response(self):
        return random.choice(self.responses)
