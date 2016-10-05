import random
import weather_manager
import logging
import traceback
import re

from channel_manager import ChannelManager
from common import ResourceManager, contains_user_tag, DONT_DELETE
from datetime import datetime, timedelta
import time

HR_DIF_DST = 5  # for Winnipeg
HR_DIF_NO_DST = 6  # for Winnipeg
MIN_PER_HOUR = 60
HR_PER_DAY = 24

TESTING_CHANNEL = 'zac-testing'


class TimeTriggeredEventManager(object):

    def __init__(self, clients, msg_writer, markov_chain):
        self.clients = clients
        self.msg_writer = msg_writer
        self.last_random_hour = 0
        self.last_random_minutes = 0
        self.random_interval_minutes = 0
        self.random_hasnt_fired = True
        self.is_just_starting_up = True
        self.markov_chain = markov_chain
        self.channel_manager = ChannelManager(clients)
        self.drunk_manager = ResourceManager('drunk_comments.txt')
        self.random_manager = ResourceManager('random_comments.txt')
        self.trigger_startup_log()
        self.add_markovs()

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
                    'user' in message and 'ts' in message and
                    self.clients.is_message_from_me(message['user'])
                ):
                    # delete everything older than 3 days old
                    if now_timestamp - (60*60*60*24*3) > float(message['ts']):
                        self.clients.delete_message(channel, message['ts'])
                        count += 1
                    # delete items older than a day old
                    # unless they are weather posts or startup logs
                    elif now_timestamp - (60*60*60*24) > float(message['ts']):
                        msg = message['text'].lower()
                        if not re.search(DONT_DELETE, msg):
                            self.clients.delete_message(channel, message['ts'])
                            count += 1
        result = "Erased " + str(count) + " messages"
        self.send_message('zac-testing', result)

    def add_markovs(self):
        channel = self.channel_manager.get_channel_id('random')
        count = 0
        response = self.clients.get_message_history(channel)
        if 'messages' in response:
            for message in response['messages']:
                if (
                    'user' in message and 'ts' in message and
                    self.clients.is_message_from_me(message['user'])
                    and not contains_user_tag(message['text'])
                ):
                    self.markov_chain.add_single_line(message['text'])
                    count += 1
        result = "Added " + str(count) + " messages to markov"
        self.send_message('zac-testing', result)

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

    def trigger_random(self):
        txt = self.random_manager.get_response()
        if random.random() <= 0.45:
            txt = str(self.markov_chain)
        self.send_message('random', txt)
        self.trigger_method_log('random')

    def check_trigger_random(self, hour, minute):
        should_fire_hr = (self.last_random_hour +
                          int(self.random_interval_minutes/MIN_PER_HOUR) +
                          int((
                            self.last_random_minutes +
                            self.random_interval_minutes % MIN_PER_HOUR
                           ) / MIN_PER_HOUR)) % HR_PER_DAY
        should_fire_min = (
            self.last_random_minutes + self.random_interval_minutes %
            MIN_PER_HOUR
        ) % MIN_PER_HOUR
        if (self.random_hasnt_fired or
                (hour == should_fire_hr and minute == should_fire_min)):
            max_minutes_between_random_events = 600  # 10 hours
            new_random_minutes = int(
                random.random() * max_minutes_between_random_events
            ) + 1
            if (hour >= 14 and hour < 18 and
                    self.random_hasnt_fired is False):
                self.trigger_random()
            self.last_random_hour = hour
            self.last_random_minutes = minute
            self.random_interval_minutes = new_random_minutes
            if self.random_hasnt_fired:
                # self.clients.upload_file_to_slack() #test file upload
                # self.clients.get_file_info()
                self.random_hasnt_fired = False

    def trigger_wine_club(self):
        tags = ['channel', 'here']
        msg = ("WINE CLUB IN THE LOUNGE :wine_glass: :wine_glass: "
               ":wine_glass: :wine_glass: :wine_glass:")
        txt = '<!{}> {}'.format(random.choice(tags), msg)
        self.send_message('random', txt)

    def trigger_drunk_phrase(self):
        drunk_comment = self.drunk_manager.get_response()
        txt = '{} :{}:'.format(drunk_comment, self.get_emoji())
        self.send_message('random', txt)

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
            # will post a ping every minute to testing channel
            self.check_trigger_random(hour, minute)
            if hour == 1 and minute == 0:
                self.clean_history()
            if hour % 3 == 0 and minute == 0:
                self.trigger_weather()
            if minute == 15:
                self.trigger_markov()
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
                if ((hour == 16 and minute == 35) or
                        (hour == 17 and minute == 0) or
                        (hour == 17 and minute == 30) or
                        (hour == 18 and minute == 0)):
                    self.trigger_drunk_phrase()


def _get_datetime():
    curr_datetime = datetime.utcnow() - timedelta(hours=HR_DIF_DST)
    day = curr_datetime.strftime('%A')
    hour = int(curr_datetime.strftime('%H'))
    minute = int(curr_datetime.strftime('%M'))
    second = int(curr_datetime.strftime('%S'))
    return day, hour, minute, second
