import json
import logging
import re

from response_master import Response_master
from user_manager import UserManager
from game_manager import GameManager
from channel_manager import ChannelManager
from markov import Markov
from common import (
    is_zac_mention, should_add_markov, should_add_loud, is_bot_message,
)

logger = logging.getLogger(__name__)


class RtmEventHandler(object):

    bold_pattern = re.compile(
        "(((?<!.)| )\*(?=\S)(?!\*).+?(?<!\*)(?<=\S)\*( |(?!.)))"
        # btw this doesn't work exactly properly
        # if you want to fix it, don't use a regex
        # this is a commit to revive zac
    )

    def __init__(self, slack_clients, msg_writer, markov_chain):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        self.game_manager = GameManager(self.msg_writer)
        self.user_manager = UserManager(self.clients, self.msg_writer)
        self.response_master = Response_master(self.msg_writer)
        self.user_manager = UserManager(self.clients, self.msg_writer)
        self.channel_manager = ChannelManager(slack_clients)

        self.markov_chain = markov_chain

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
        elif (
            event_type == 'reaction_added' and 'user' in event and
            not self.clients.is_message_from_me(event)
        ):
            if 'channel' in event['item']:
                msg = event['item']
                self.response_master.process_reaction(
                    event['reaction'], msg['channel'], msg['ts']
                )
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
            # if self._is_edited_by_user(event):
            #     self.msg_writer.write_spelling_mistake(
            #         event['channel'], event['message']['ts']
            #     )
            if (
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
            logging.info("Handling event")

            msg_txt = event['text']
            channel_id = event['channel']
            user_id = event['user']
            ts = event['ts']

            user_name = self.user_manager.get_user_by_id(user_id)
            lower_txt = msg_txt.lower()

            # Markov chain addition and response
            if should_add_markov(event):
                self.markov_chain.add_single_line(msg_txt)
            if (
                channel_id == self.channel_manager.get_channel_id('markov') or
                lower_txt == 'markov'
            ):
                self.msg_writer.send_message(str(self.markov_chain), channel_id)

            # Respond to messages handled by response_manager
            self.response_master.process_message(
                msg_txt, channel_id, user_id, ts
            )

            # Command line
            # logging.info("lower_txt: "+str(lower_txt.split()))
            try:
                token = lower_txt.split()[0]
                if token == '#>' or token == u'#&gt;':
                    # logging.info("entering terminal command mode")
                    self.msg_writer.write_terminal_command(
                        lower_txt, channel_id
                    )
                    return 0  # Do not continue execution
            except:
                pass

            # Return channel and user information
            if lower_txt == 'channelinfo':
                self.msg_writer.send_message(channel_id, channel_id)
            elif lower_txt == 'channelname':
                self.msg_writer.send_message(
                    self.channel_manager.get_channel_by_id(channel_id),
                    channel_id
                )
            elif lower_txt == 'userinfo':
                self.msg_writer.send_message(user_id, channel_id)
            elif lower_txt == 'allusersinfo':
                self.user_manager.print_all_users(channel_id)
            elif lower_txt == 'allchannelinfo':
                self.msg_writer.send_message(
                    str(self.channel_manager.get_all_channel_ids()),
                    channel_id
                )
            elif lower_txt == 'allchannelname':
                self.msg_writer.send_message(
                    str(self.channel_manager.get_all_channel_names()),
                    channel_id
                )

            # Loud addition and response
            if should_add_loud(event):
                self.msg_writer.write_loud(msg_txt)
                self.msg_writer.respond_loud(msg_txt, channel_id)

            # Respond to message text
            if re.search('i choose you', lower_txt):
                self.msg_writer.write_cast_pokemon(lower_txt, channel_id)
            if re.search('riri', lower_txt):
                self.msg_writer.write_riri_me(msg_txt, channel_id)

            # Respond to message text with `zac` included
            if is_zac_mention(msg_txt) or self.clients.is_bot_mention(msg_txt):
                if re.search('weather', lower_txt):
                    self.msg_writer.write_weather(channel_id)
                if re.search('erase|delete', lower_txt):
                    self.msg_writer.erase_history(
                        msg_txt, channel_id, ts
                    )
                if 'help' in lower_txt:
                    self.msg_writer.write_help_message(channel_id)
                if 'french' in lower_txt:
                    self.msg_writer.write_french(msg_txt, channel_id)
                if re.search('who\'?s that pokemon', msg_txt):
                    self.msg_writer.write_whos_that_pokemon(channel_id)
                if re.search(' ?zac it\'?s', lower_txt):
                    self.msg_writer.write_pokemon_guessed_response(
                        msg_txt, channel_id, user_id
                    )
                if re.search('attachment|beep boop link', lower_txt):
                    self.msg_writer.demo_attachment(channel_id)
                if 'sass ' in lower_txt:
                    self.msg_writer.write_sass(msg_txt, channel_id)
                if 'solve' in lower_txt:
                    self.msg_writer.write_solution(msg_txt, channel_id)
                if re.search('explain|why', lower_txt):
                    self.msg_writer.write_explanation(channel_id)
                if re.search('sweetpotato|sweet potato', lower_txt):
                    self.msg_writer.write_sweetpotato_me(msg_txt, channel_id)
                if lower_txt == "zac":
                    self.msg_writer.write_prompt(channel_id)
                # The word google must be specified in lower case
                if 'zac google ' in msg_txt:
                    self.msg_writer.google(msg_txt, channel_id)
                else:
                    pass
