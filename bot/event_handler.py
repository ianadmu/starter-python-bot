import json
import logging
import re

from response_master import Response_master
from tictactoe_manager import TicTacToeManager
from user_manager import UserManager
from game_manager import GameManager
from rude_manager import RudeManager
from channel_manager import ChannelManager
from markov import Markov
from common import (
    is_zac_mention, should_add_markov, should_add_loud, is_bot_message,
)

logger = logging.getLogger(__name__)


class RtmEventHandler(object):

    bold_pattern = re.compile(
        "(((?<!.)| )\*(?=\S)(?!\*).+?(?<!\*)(?<=\S)\*( |(?!.)))"
    )

    def __init__(self, slack_clients, msg_writer, markov_chain):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        self.game_manager = GameManager(self.msg_writer)
        self.user_manager = UserManager(self.clients, self.msg_writer)
        self.tictactoe_manager = TicTacToeManager(
            self.msg_writer, self.user_manager, self.game_manager
        )
        self.response_master = Response_master(self.msg_writer)
        self.user_manager = UserManager(self.clients, self.msg_writer)
        self.rude_manager = RudeManager(self.msg_writer)
        self.channel_manager = ChannelManager(slack_clients)

        self.markov_chain = markov_chain
        self.lotrMarkov = Markov(2, msg_writer)
        self.lotrMarkov.add_file('hpOne.txt')
        self.lotrMarkov.add_file('lotrOne.txt')
        self.lotrMarkov.add_file('memoriesOfIce.txt')

    def handle(self, event):
        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            self.msg_writer.write_error(json.dumps(event), event['channel'])
        elif event_type == 'message':
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel']['id'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'reaction_added':
            if 'channel' in event['item']:
                self.response_master.get_emoji_response(
                    event['item']['channel'], event['reaction'])
        else:
            pass

    def _is_edited_with_star(self, message):
        return '*' in re.sub(self.bold_pattern, '', message)

    def _is_edited_by_user(self, event):
        if 'subtype' in event:
            if event['subtype'] == 'message_changed':
                if 'message' in event:
                    event_msg = event['message']

                    # Dont allow zac to spam his own message edits
                    if self.clients.is_message_from_me(event_msg):
                        return False

                    if (
                        'user' in event_msg and 'edited' in event_msg and
                        'user' in event_msg['edited'] and
                        not is_bot_message(event_msg['edited'])
                    ):
                        user1 = event_msg['user']
                        user2 = event_msg['edited']['user']
                    return user1 == user2
        return False

    def _handle_message(self, event):
        if 'subtype' in event:
            if self._is_edited_by_user(event):
                self.msg_writer.write_spelling_mistake(
                    event['channel'], event['message']['ts']
                )
            elif (
                event['subtype'] == 'channel_join' and
                not self.clients.is_message_from_me(event)
            ):
                self.msg_writer.write_joined_channel(
                    event['channel'], event['user']
                )
            elif event['subtype'] == 'message_deleted':
                self.msg_writer.write_message_deleted(event['channel'])
            elif event['subtype'] == 'channel_leave':
                self.msg_writer.write_left_channel(event['channel'])

        # Filter out messages from the bot itself
        if 'user' in event and not self.clients.is_message_from_me(event):
            # Do admin
            msg_txt = event['text']
            channel = event['channel']
            user = event['user']
            user_name = self.user_manager.get_user_by_id(user)
            lower_txt = msg_txt.lower()

            # Markov chain addition and response
            if should_add_markov(event):
                self.markov_chain.add_single_line(msg_txt)
            if (
                channel == self.channel_manager.get_channel_by_name('markov')
                or lower_txt == 'markov'
            ):
                self.msg_writer.send_message(channel, str(self.lotrMarkov))

            # Respond to messages handled by rude_manager and response_manager
            self.rude_manager.run(channel, user)
            self.response_master.give_message(channel, msg_txt, user)

            # Return channel and user information
            if lower_txt == 'channelinfo':
                self.msg_writer.send_message(channel, channel)
            if lower_txt == 'userinfo':
                self.msg_writer.send_message(channel, user)
            if lower_txt == 'allusersinfo':
                self.user_manager.print_all_users(channel)

            # Loud addition and response
            if should_add_loud(event):
                self.msg_writer.write_loud(msg_txt)
                self.msg_writer.respond_loud(channel, msg_txt)
            if self._is_edited_with_star(msg_txt):
                self.msg_writer.write_spelling_mistake(channel, event['ts'])

            # Respond to message text
            if re.search('i choose you', lower_txt):
                self.msg_writer.write_cast_pokemon(channel, lower_txt)
            if re.search('weather', lower_txt):
                self.msg_writer.write_weather(channel)
            if re.search('riri', lower_txt):
                self.msg_writer.write_riri_me(channel, msg_txt)
            if re.search('encourage me', lower_txt):
                self.msg_writer.write_encouragement(channel, user)
            if 'xkcd' in lower_txt:
                requestedComic = lower_txt[lower_txt.find('xkcd') + 4:]
                self.msg_writer.write_xkcd(channel, requestedComic)
            if 'tictactoe' in lower_txt or 'ttt' in lower_txt:
                self.tictactoe_manager.get_message(
                    channel, lower_txt, user_name
                )

            # Respond to message text with `zac` included
            if is_zac_mention(msg_txt) or self.clients.is_bot_mention(msg_txt):
                if 'erase' in lower_txt:
                    self.msg_writer.erase_history(
                        channel, event['ts'], msg_txt
                    )
                if re.search('night', lower_txt):
                    self.msg_writer.write_good_night(channel, user)
                if 'help' in lower_txt:
                    self.msg_writer.write_help_message(channel)
                if 'joke' in lower_txt:
                    self.msg_writer.write_joke(channel)
                if 'french' in lower_txt:
                    self.msg_writer.write_french(channel, msg_txt)
                if re.search('who\'?s that pokemon', msg_txt):
                    self.msg_writer.write_whos_that_pokemon(channel)
                if re.search(' ?zac it\'?s', lower_txt):
                    self.msg_writer.write_pokemon_guessed_response(
                        channel, user, msg_txt
                    )
                if re.search('attachment|beep boop link', lower_txt):
                    self.msg_writer.demo_attachment(channel)
                if 'sad' in lower_txt:
                    self.msg_writer.write_sad(channel)
                if 'sort me' in lower_txt:
                    self.msg_writer.write_hogwarts_house(
                        channel, user,  msg_txt
                    )
                if 'sass ' in lower_txt:
                    self.msg_writer.write_sass(channel, msg_txt)
                if 'solve' in lower_txt:
                    self.msg_writer.write_solution(channel, msg_txt)
                if re.search('explain|why', lower_txt):
                    self.msg_writer.write_explanation(channel)
                if re.search('sweetpotato me|sweet potato me', lower_txt):
                    self.msg_writer.write_sweetpotato_me(channel, user)
                if re.search('draw me', lower_txt):
                    self.msg_writer.write_draw_me(channel)
                if re.search('love|forever|relationship', lower_txt):
                    self.msg_writer.write_forever(channel)
                if re.search('unflip', lower_txt):
                    self.msg_writer.write_unflip(channel)
                elif re.search('flip|rageflip', lower_txt):
                    self.msg_writer.write_flip(channel)
                if re.search('sup son', lower_txt):
                    self.msg_writer.write_sup_son(channel)
                if lower_txt == "zac":
                    self.msg_writer.write_prompt(channel)
                else:
                    pass
