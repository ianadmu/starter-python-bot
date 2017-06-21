# coding=utf-8

import logging
import random
import re
import weather_manager
import terminal_manager
import requests

from channel_manager import ChannelManager
from loud_manager import LoudManager
from whos_that_pokemon_manager import WhosThatPokemonManager
from equation_manager import EquationManager
from common import (
    ResourceManager, is_zac_mention, get_target,
    TESTING_CHANNEL, TEAM_MATES, DONT_DELETE,
)

SASS_FLAG = re.compile('sass[a-z]* ')
ENCOURAGE_FLAG = re.compile('encourage[a-z]* ')
FRENCH_FLAG = re.compile('french[a-z]* ')
SWEETPOTATO_FLAG = re.compile('sweet ?potato[a-z]* ')
RIRI_FLAG = re.compile('riri[a-z]* ')
GOOGLE_FLAG = re.compile('google[a-z]*')

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.loud_manager = LoudManager()
        self.whos_that_pokemon_manager = WhosThatPokemonManager()
        self.equation_manager = EquationManager()
        self.explanation_manager = ResourceManager('explanations.txt')
        self.help_manager = ResourceManager('help_text.txt')
        self.sass_manager = ResourceManager('sass.txt')
        self.channel_manager = ChannelManager(slack_clients)

    def erase_history(self, msg_text, channel_id, now_timestamp):
        try:
            tokens = re.findall('[0-9]+', msg_text)
            delete_num = int(tokens[0])
            count = 0
            response = self.clients.get_message_history(channel_id)
            if 'messages' in response:
                for message in response['messages']:
                    if (
                        'ts' in message and 'pinned_to' not in message and
                        self.clients.is_message_from_me(message) and
                        not re.search(DONT_DELETE, message['text'].lower())
                    ):
                        response = self.clients.delete_message(
                            channel_id, message['ts']
                        )
                        count += 1
                        if count >= delete_num:
                            break
            if count < delete_num:
                msg = ("Erased " + str(count) + " messages: I "
                       "can only see the 100 most recent messages")
                self.send_message(msg, channel_id)
        except Exception:
            msg = "Correct usage is `zac erase <num>`"
            self.send_message(msg, channel_id)
            pass

    def __del__(self):
        closing_msgs = ["No!! Don't kill me! I want to live!", "Good BYEEE!!!",
                        "I'm dying again :sob:",
                        "Have you gotten tired of this face :zacefron: ?"]
        txt = random.choice(closing_msgs)
        self.send_message(txt)

    def send_slow_message_as_other(self, msg_text, channel, username, emoji):
        self.send_message_as_other(
            msg_text, channel, username, emoji, slow=True
        )

    def send_message_as_other(
        self, msg_text, channel, username, emoji, slow=False
    ):
        msg_text = msg_text.replace('&', "&amp;")
        channel = self.channel_manager.get_channel_id(channel)
        if (slow):
            self.clients.send_user_typing_pause(channel)

        return self.clients.send_message_as_other(
            msg_text, channel, username, emoji
        )

    def write_slow(self, msg_text, channel=None):
        return self.send_message(msg_text, channel, slow=True)

    def send_message(
        self, msg_text, channel=None, slow=False, react_emoji=None
    ):
        msg_text = msg_text.replace('&', "&amp;")
        msg_text = msg_text.replace('&quot;', "\"")

        # channel = self.channel_manager.get_channel_id(channel)

        if channel is None:
            channel = TESTING_CHANNEL
        if slow is True:
            self.clients.send_user_typing_pause(channel)
        response = self.clients.send_message(msg_text, channel)
        if 'ok' in response and react_emoji is not None:
            self.send_reaction(react_emoji, channel, response['ts'])

        return response

    def update_message(
        self, updated_msg_text, ts, channel=None, slow=False, react_emoji=None
    ):
        updated_msg_text = updated_msg_text.replace('&', "&amp;")

        channel = self.channel_manager.get_channel_id(channel)

        if channel is None:
            channel = TESTING_CHANNEL
        if slow is True:
            self.clients.send_user_typing_pause(channel)
        response = self.clients.update_message(
            updated_msg_text, channel, ts
        )
        if 'ok' in response and react_emoji is not None:
            self.send_reaction(react_emoji, channel, response['ts'])
        return response

    def send_attachment(self, txt, channel_id, attachment):
        self.clients.send_attachment(txt, channel_id, attachment)

    def write_error(self, err_msg, channel_id=None):
        txt = (":face_with_head_bandage: my maker didn't handle this error "
               "very well:\n>```{}```").format(err_msg)
        self.send_message(txt, channel_id)

    def send_reaction(self, emoji_name, channel_id, timestamp):
        self.clients.send_reaction(emoji_name, channel_id, timestamp)

    def get_emoji(self):
        return self.clients.get_random_emoji()

    def write_message_deleted(self, channel_id):
        # Dont post if messages were deleted inside of #zac-testing
        if channel_id != self.channel_manager.get_channel_id('zac-testing'):
            txt = ("I SAW THAT! _Someone_ deleted a message from channel: "
                   "<#{}>").format(channel_id)
            self.send_message(txt)

    def write_left_channel(self, channel_id):
        self.send_message('...well THAT was something', channel_id)

    def write_joined_channel(self, channel_id, user_id):
        if channel_id == self.channel_manager.get_channel_id('zac-testing'):
            txt = ("Hey <@{}>! Welcome to the Testing (aka the Weather) "
                   "channel. Please MUTE this channel or be inundaded with "
                   "notifications!").format(user_id)
            self.write_slow(txt, channel_id)
        else:
            self.write_greeting(channel_id, user_id)

    def write_help_message(self, channel_id):
        help_txt = self.help_manager.get_all()
        count = self.help_manager.get_count()
        txt = (
            "I'm Zac.  I'll *_respond_* to the following {} commands:\n{}"
        ).format(count-1, help_txt)
        info_text = (
            "Hi, I'm Zac Efron. You can find out more information about me "
            "in #zac-testing. Merci :zacefron:"
        )
        self.write_slow(info_text, channel_id)
        self.write_slow(txt, 'zac-testing')

    def write_french(self, msg_text, channel_id):
        target = get_target(FRENCH_FLAG, msg_text).replace('_', '')
        self.write_slow('_le {}_'.format(target), channel_id)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.write_slow(txt, channel_id)

    def write_spelling_mistake(self, channel_id, timestamp):
        emoji_name = "spelft_it_wronbg_again_i_see"
        self.send_reaction(emoji_name, channel_id, timestamp)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = ("I'm sorry, I didn't quite understand... Can I help you? "
               "(e.g. `<@" + bot_uid + "> help`)")
        self.write_slow(txt, channel_id)

    def write_cast_pokemon(self, lower_msg_text, channel_id):
        pkmn = pokemon_i_choose_you(lower_msg_text)
        if pkmn is not None:
            self.send_message(pkmn, channel_id)

    def write_whos_that_pokemon(self, channel_id):
        txt = self.whos_that_pokemon_manager.whos_that_pkmn()
        self.send_message(txt, channel_id)

    def write_pokemon_guessed_response(self, msg_text, channel_id, user_id):
        text = self.whos_that_pokemon_manager.check_response(user_id, msg_text)
        if text is not None:
            self.send_message(text, channel_id)

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
        self.send_attachment(txt, channel_id, attachment)

    def write_weather(self, channel_id):
        self.write_slow(weather_manager.getCurrentWeather(), channel_id)

    def write_loud(self, orig_msg):
        if not is_zac_mention(orig_msg):
            self.loud_manager.write_loud_to_file(orig_msg)

    def respond_loud(self, orig_msg, channel_id):
        if is_zac_mention(orig_msg) or random.random() < 0.8:
            message = self.loud_manager.get_random_loud();
            
            if message:
                self.send_message(self.loud_manager.get_random_loud(), channel_id)

    def write_explanation(self, channel_id):
        self.write_slow(self.explanation_manager.get_response(), channel_id)

    def write_sass(self, msg_txt, channel_id):
        target = get_target(SASS_FLAG, msg_txt)
        sass = 'Hey, {}! {}'.format(target, self.sass_manager.get_response())
        self.write_slow(sass, channel_id)

    def write_solution(self, msg_text, channel_id):
        self.write_slow(self.equation_manager.solve(msg_text), channel_id)

    def write_sweetpotato_me(self, msg_text, channel_id):
        target = get_target(SWEETPOTATO_FLAG, msg_text)
        txt = 'Here, {}! :sweet_potato:'.format(target)
        self.write_slow(txt, channel_id)

    def write_riri_me(self, msg_text, channel_id):
        target = get_target(RIRI_FLAG, msg_text).upper()
        if target != "":
            txt = ' '.join(target for num in range(5))
        else:
            txt = "WHY WOULD YOU JUST TYPE RIRI?\n"
        self.write_slow(txt, channel_id)

    def write_terminal_command(self, lower_msg_text, channel_id):
        response = terminal_manager.run_terminal_command(lower_msg_text)
        self.send_message(response, channel_id)

    def google(self, msg_text, channel_id):
        try:
            tokens = re.split(GOOGLE_FLAG, msg_text)
            query = ""
            for num in range(len(tokens)):
                if num > 0:
                    query += "+" + tokens[num].strip()
            if len(query) > 1:
                query = query[1:]

            url = (
                "https://www.googleapis.com/customsearch/v1?key=AIzaSyDs8-"
                "StJem2hqcu2L-J4PceBPVx5Jk6txk&cx=004179257401026011423:y4"
                "vp3hnjgvo&q="
            ) + query

            response = requests.get(url).json()
            result = response['items'][0]['link']

            self.send_message(result, channel_id)
        except Exception as e:
            self.write_error(str(e))


def pokemon_i_choose_you(lower_msg_text):
    target = lower_msg_text.split()[0]
    if re.search(TEAM_MATES, target.lower()):
        return "Go! {}!\n:{}:".format(target.title(), target)
    elif target.lower() == "sleep":
        return "Go! {}!\n:{}:".format(target.title(), 'bed')
    else:
        link = 'http://pokeapi.co/api/v2/pokemon/{}/'
        pkmn = link.format(target)
        try:
            response = requests.get(pkmn)
        except requests.exceptions.RequestException:
            return None
        else:
            pokemon = response.json()
            if 'sprites' in pokemon:
                result = "Go! {}!\n{}".format(
                    target.title(), pokemon['sprites']['front_default']
                )
                return result

