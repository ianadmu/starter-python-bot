import random
import weather_manager
import logging
import traceback
import re

from channel_manager import ChannelManager
from common import (
    ResourceManager, contains_tag, DONT_DELETE,
    is_loud, TESTING_CHANNEL, should_add_markov
)
from datetime import datetime, timedelta
import time

HR_DIF_DST = 5  # for Winnipeg
HR_DIF_NO_DST = 6  # for Winnipeg
MIN_PER_HOUR = 60
HR_PER_DAY = 24


class TimeTriggeredEventManager(object):

    def __init__(self, clients, msg_writer, markov_chain):
        self.clients = clients
        self.msg_writer = msg_writer
        self.markov_chain = markov_chain
        self.channel_manager = ChannelManager(clients)
        self.random_manager = ResourceManager('random_comments.txt')
        self.trigger_startup_log()
        self.process_recent_messages()

    def send_message(self, channel, msg_txt):
        self.msg_writer.send_message(channel, msg_txt)

    def get_emoji(self):
        return self.clients.get_random_emoji()

    def clean_history(self):
        channel = self.channel_manager.get_channel_id('zac-testing')
        count = 0
        now_timestamp = float(time.time())
        response = self.clients.get_message_history(channel)
        if 'messages' in response:
            for message in response['messages']:
                if (
                    'ts' in message and 'pinned_to' not in message and
                    self.clients.is_message_from_me(message)
                ):
                    # Delete everything older than 2 days old
                    # Delete items older than a day old
                    # Unless they are weather posts or startup logs
                    if (
                        (now_timestamp - (60*60*24*2)) > float(message['ts'])
                        or (
                            (now_timestamp - (60*60*24)) > float(message['ts'])
                            and not re.search(
                                DONT_DELETE, message['text'].lower()
                            )
                        )
                    ):
                        self.clients.delete_message(channel, message['ts'])
                        count += 1
        result = "Erased " + str(count) + " messages"
        self.send_message('zac-testing', result)

    def process_recent_messages(self):
        try:
            testing_channel = self.channel_manager.get_channel_id(TESTING_CHANNEL)
            count_markov = 0
            count_louds = 0
            for channel_id in self.channel_manager.get_all_channel_ids():
                if channel_id != testing_channel:
                    response = self.clients.get_message_history(channel_id)
                    if 'messages' in response:
                        for message in response['messages']:
                            if not self.clients.is_message_from_me(message):
                                msg_text = message['text']

                                # Add markovs
                                if should_add_markov(message):
                                    self.markov_chain.add_single_line(msg_text)
                                    count_markov += 1

                                # Add louds
                                if is_loud(message):
                                    self.msg_writer.write_loud(msg_text)
                                    count_louds += 1

            result = (
                "Added " + str(count_markov) + " messages to markov\n"
                "Added " + str(count_louds) + " loud messages"
            )
            self.send_message(TESTING_CHANNEL, result)
        except Exception:
            err_msg = traceback.format_exc()
            logging.error('Unexpected error: {}'.format(err_msg))
            self.msg_writer.write_error(err_msg)
            pass

    def trigger_random_markov(self):
        if random.random() < 0.15:
            channel_id = self.channel_manager.get_channel_id('random')
            now_timestamp = float(time.time())
            response = self.clients.get_message_history(channel_id, 1)
            if 'messages' in response:
                for message in response['messages']:
                    if (
                        'user' in message and 'ts' in message and not
                        self.clients.is_message_from_me(message)
                        and not contains_tag(message['text'])
                        and 'markov' not in message['text']
                    ):
                        # Post only 3 - 5 minutes after latest message
                        if (
                            now_timestamp - (60*5) <= float(message['ts']) and
                            now_timestamp - (60*2) >= float(message['ts'])
                        ):
                            try:
                                txt = str(self.markov_chain)
                                self.send_message('random', txt)
                                self.trigger_method_log('random markov')
                            except Exception:
                                err_msg = traceback.format_exc()
                                logging.error(
                                    'Unexpected error: {}'.format(err_msg)
                                )
                                self.msg_writer.write_error(err_msg)
                                pass

    def trigger_morning(self):
        responses = ["Good morning", "Morning", "Guten Morgen", "Bonjour",
                     "Ohayou", "Good morning to you", "Aloha",
                     "Konnichiwashington", "Buenos dias", "GLUTEN MORNING"
                     ":sunny: Good morning", "Where have you been. MORNING"]
        txt = '{}! :{}:'.format(random.choice(responses), self.get_emoji())
        self.send_message('random', txt)

    def trigger_markov(self):
        try:
            self.msg_writer.send_message('markov', str(self.markov_chain))
        except Exception:
            err_msg = traceback.format_exc()
            logging.error('Unexpected error: {}'.format(err_msg))
            self.msg_writer.write_error(err_msg)
            pass

    def trigger_ping(self, day, hour, minute, second):
        msg = ('Ping on ' + day + ' ' + str(hour) + ':' + str(minute) +
               ':' + str(second) + ' :' + str(self.get_emoji()) + ':')
        self.send_message(TESTING_CHANNEL, msg)

    def trigger_method_log(self, method_name):
        msg = 'Event: {}'.format(method_name)
        self.send_message(TESTING_CHANNEL, msg)

    def trigger_startup_log(self):
        day, hour, minute, second = _get_datetime()
        msg = ('I came back to life on ' + day + ' ' + str(hour) + ':' +
               str(minute) + ':' + str(second) + ' :' + str(self.get_emoji()) +
               ':')
        self.send_message(TESTING_CHANNEL, msg)

    def trigger_wine_club(self):
        tags = ['channel', 'here']
        msg = ("WINE CLUB IN THE LOUNGE :wine_glass: :wine_glass: "
               ":wine_glass: :wine_glass: :wine_glass:")
        txt = '<!{}> {}'.format(random.choice(tags), msg)
        self.send_message('random', txt)

    def trigger_random_phrase(self):
        if random.random() < 0.005:
            comment = self.random_manager.get_response()
            txt = '{} :{}:'.format(comment, self.get_emoji())
            self.send_message('random', txt)
            self.trigger_method_log('wine club')

    def trigger_weather(self):
        response = weather_manager.getCurrentWeather()
        self.send_message(TESTING_CHANNEL, response)

    def trigger_945(self):
        kip_msgs = ['@945', '945!', '#945', ':paw_prints: 945!', '~945~',
                    ':horse: 945! giddyup', '945! :heart:',
                    '945! :sweet_potato:', '945!........', '945 time',
                    '945 quickie', '945 o\'clock',
                    '945! :sheep: :panda_face: :slowpoke:', '945! :boom:',
                    ':eggplant: 945.', '945 :coffee:', '_le 945_',
                    '_le fast 945_']
        txt = '{} :{}:'.format(random.choice(kip_msgs), self.get_emoji())
        self.send_message('random', txt)

    def trigger_mochaccino(self):
        msgs = ['The mochaccino tastes _amazing_ this morning!',
                'Eh, mochaccino ain\'t so great today...',
                'HELP! MOCHACCINO EVERYWHERE!',
                ('The mochaccino machine won\'t stop dripping help I need an '
                    'adult'),
                'WHAT! wHY is my mochaccino _decaf_??!',
                'I haven\'t had my mochaccino yet don\'t talk to me',
                'WHERE\'S MY MUG I NEED MOCHACCINO!!',
                'Mochaccino mochaccino mochaccino',
                'Mochaccino is SO GOOD TODAY HOLY HELL',
                ('Today\'s mochaccino is like an angel pooped out a nice hot '
                    'cup of coffee mmmmm~'),
                'Mochaccino status: passable',
                'MOCHACCINO MOCHACCINO MOCHACCINO!!!',
                'Who\'s ready for a nice cup o\' mochaccino?',
                '_le mochaccino_']
        txt = '{} :coffee:'.format(random.choice(msgs))
        self.send_message('random', txt)

    def trigger_timed_event(self):
        day, hour, minute, second = _get_datetime()

        # leaves 10-ish seconds to trigger since method is called every 10-ish
        # seconds and we wantz the if statement to trigger once per min only
        if(second >= 5 and second <= 15):
            # self.trigger_ping(day, hour, minute, second)
            if hour == 1 and minute == 0:
                self.clean_history()
            if hour % 3 == 0 and minute == 0:
                self.trigger_weather()
            if minute == 15:
                self.trigger_markov()
            if hour >= 9 and hour <= 16:
                self.trigger_random_markov()
            if (day != 'Saturday' and day != 'Sunday'):
                if hour == 8 and minute == 45:
                    self.trigger_morning()
                if hour == 9:
                    if minute == 45:
                        self.trigger_945()
                    elif minute == 0:
                        self.trigger_mochaccino()
            if day == 'Friday':
                if hour == 16 and minute == 30:
                    self.trigger_wine_club()
                if hour >= 17 and hour <= 18:
                    self.trigger_random_phrase()


def _get_datetime():
    curr_datetime = datetime.utcnow() - timedelta(hours=HR_DIF_DST)
    day = curr_datetime.strftime('%A')
    hour = int(curr_datetime.strftime('%H'))
    minute = int(curr_datetime.strftime('%M'))
    second = int(curr_datetime.strftime('%S'))
    return day, hour, minute, second
