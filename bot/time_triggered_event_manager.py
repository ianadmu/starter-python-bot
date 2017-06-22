import random
import weather_manager
import logging
import traceback
import re

from channel_manager import ChannelManager
from common import (
    ResourceManager, contains_tag, DONT_DELETE,
    should_add_loud, TESTING_CHANNEL, should_add_markov,
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
        self.trigger_startup_log()
        self.process_recent_messages()

    def send_message(self, msg_txt, channel=None):
        self.msg_writer.send_message(msg_txt, channel)

    def get_emoji(self):
        return self.clients.get_random_emoji()

    def clean_channels_history(self):
        result = 'Erased messages: '
        testing_channel = self.channel_manager.get_channel_id(TESTING_CHANNEL)
        for channel_id in self.channel_manager.get_all_channel_ids():
            if channel_id != testing_channel:
                count = self._erase_channel_messages(channel_id, log_days=3)
                if count != 0:
                    result += '<#{}> ({}), '.format(
                        str(channel_id), str(count)
                    )
        if result.endswith(', '):
            result = result[:-2]
        else:
            result = 'No messages erased during general clean up'
        self.send_message(result)

    def clean_testing_channel_history(self):
        testing_channel = self.channel_manager.get_channel_id(TESTING_CHANNEL)
        total_count = 0
        for num in range(10):
            count = self._erase_channel_messages(testing_channel, log_days=1)
            total_count += count
            if count == 0:
                break
        result = 'Erased {} total messages from <#{}> in {} passes'.format(
            str(total_count), str(testing_channel), str(num)
        )
        self.send_message(result)

    def _erase_channel_messages(self, channel_id, log_days=0):
        count = 0
        now_ts = float(time.time())
        response = self.clients.get_message_history(channel_id)
        if 'messages' in response:
            for message in response['messages']:
                if (
                    'ts' in message and 'pinned_to' not in message and
                    self.clients.is_message_from_me(message)
                ):
                    # Delete everything older than `log_days` old
                    # Delete items older than a day old
                    # Unless they are weather posts or startup logs
                    # Always delete the message deletions messages
                    if (
                        (now_ts - (60*60*24*log_days)) > float(message['ts'])
                        or (
                            (now_ts - (60*60*24)) > float(message['ts'])
                            and not re.search(
                                DONT_DELETE, message['text'].lower()
                            )
                            or (
                                re.search(
                                    "I SAW THAT! _Someone_ deleted a message",
                                    message['text']
                                )
                            )
                        )
                    ):
                        self.clients.delete_message(channel_id, message['ts'])
                        count += 1
        return count

    def process_recent_messages(self):
        testing_channel = self.channel_manager.get_channel_id(TESTING_CHANNEL)
        count_markov = 0
        count_louds = 0
        for channel_id in self.channel_manager.get_all_channel_ids():
            if channel_id != testing_channel:
                response = self.clients.get_message_history(channel_id)
                if 'messages' in response:
                    for message in response['messages']:
                        if not self.clients.is_message_from_me(message):
                            if 'text' in message:
                                msg_text = message['text']

                                # Add markovs
                                if should_add_markov(message):
                                    self.markov_chain.add_single_line(msg_text)
                                    count_markov += 1

                                # Add louds
                                if should_add_loud(message):
                                    self.msg_writer.write_loud(msg_text)
                                    count_louds += 1
        result = (
            "Added " + str(count_markov) + " messages to markov "
            "and " + str(count_louds) + " loud messages"
        )
        self.send_message(result)

    def trigger_random_markov(self, channel):
        if random.random() < 0.15:
            channel_id = self.channel_manager.get_channel_id(channel)
            now_timestamp = float(time.time())
            response = self.clients.get_message_history(channel_id, 1)
            if 'messages' in response:
                for message in response['messages']:
                    if (
                        'user' in message and 'ts' in message and not
                        self.clients.is_message_from_me(message) and
                        not contains_tag(message['text']) and
                        'markov' not in message['text']
                    ):
                        # Post only 3 - 5 minutes after latest message
                        if (
                            now_timestamp - (60*5) <= float(message['ts']) and
                            now_timestamp - (60*2) >= float(message['ts'])
                        ):
                            try:
                                txt = str(self.markov_chain)
                                self.send_message(txt, channel)
                                self.trigger_method_log('random markov')
                            except Exception:
                                err_msg = traceback.format_exc()
                                logging.error(
                                    'Unexpected error: {}'.format(err_msg)
                                )
                                self.msg_writer.write_error(err_msg)
                                pass

    def trigger_ping(self, day, hour, minute, second):
        msg = ('Ping on ' + day + ' ' + str(hour) + ':' + str(minute) +
               ':' + str(second) + ' :' + str(self.get_emoji()) + ':')
        self.send_message(msg)

    def trigger_method_log(self, method_name):
        msg = 'Event: {}'.format(method_name)
        self.send_message(msg)

    def trigger_startup_log(self):
        day, hour, minute, second = _get_datetime()
        msg = ('I came back to life on ' + day + ' ' + str(hour) + ':' +
               str(minute) + ':' + str(second) + ' :' + str(self.get_emoji()) +
               ':')
        self.send_message(msg)

    def trigger_weather(self):
        response = weather_manager.getCurrentWeather()
        self.send_message(response)

    def trigger_tuesday(self):
        txt = "DON'T FORGET IT'S TUESDAY _ALLL_ DAY TODAY"
        self.msg_writer.send_message_as_other(
            txt, 'random', 'zac', ':rolled_up_newspaper:'
        )

    def trigger_timed_event(self):
        day, hour, minute, second = _get_datetime()

        # leaves 10-ish seconds to trigger since method is called every 10-ish
        # seconds and we want the if statement to trigger once per min only
        if(second >= 5 and second <= 16):
            try:
                # self.trigger_ping(day, hour, minute, second)
                if hour == 1:
                    if minute == 15:
                        self.clean_channels_history()
                    if minute == 0 or minute == 30:
                        self.clean_testing_channel_history()
                if hour % 3 == 0 and minute == 0:
                    self.trigger_weather()
                if hour >= 9 and hour <= 16:
                    self.trigger_random_markov('random')
                    self.trigger_random_markov('work')
                if day == 'Tuesday' and hour == 14 and minute == 43:
                    self.trigger_tuesday()
            except Exception as e:
                self.msg_writer.write_error(e)



def _get_datetime():
    curr_datetime = datetime.utcnow() - timedelta(hours=HR_DIF_NO_DST)
    day = curr_datetime.strftime('%A')
    hour = int(curr_datetime.strftime('%H'))
    minute = int(curr_datetime.strftime('%M'))
    second = int(curr_datetime.strftime('%S'))
    return day, hour, minute, second
