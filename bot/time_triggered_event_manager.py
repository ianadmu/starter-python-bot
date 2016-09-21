import random
import json
import os.path
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import weather_manager
import scripts.weather_controller
from scripts.weather_controller import WeatherController
import common

HOUR_DIFFERENCE_DAYLIGHT_SAVINGS = 5 #for Winnipeg
HOUR_DIFFERENCE_NO_DAYLIGHT_SAVINGS = 6 #for Winnipeg
MIN_PER_HOUR = 60
HR_PER_DAY = 24

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

    def trigger_markov(self):
        self.msg_writer.send_message('C244LFHS7', str(self.markov_chain))

    def trigger_ping(self, day, hour, minute, second):
        random_custom_emoji = self.clients.get_random_emoji()
        msg = 'Ping on ' + day + ' ' + str(hour)  + ':' + str(minute) + ':' + str(second) + ' :' + str(random_custom_emoji) + ':'
        self.msg_writer.send_message('C1SDALDG9', msg)

    def trigger_method_log(self, method_name):
        msg = 'Event: {}'.format(method_name)
        try:
            self.msg_writer.send_message(common.channels['slackers']['zac-testing'], msg)
        except:
            self.msg_writer.send_message(common.channels['iq']['zac-testing'], msg)

    def trigger_startup_log(self, day, hour, minute, second):
        random_custom_emoji = self.clients.get_random_emoji()
        msg = 'I came back to life on ' + day + ' ' + str(hour)  + ':' + str(minute) + ':' + str(second) + ' :' + str(random_custom_emoji) + ':'
        try:
            self.msg_writer.send_message(common.channels['slackers']['zac-testing'], msg)
        except:
            self.msg_writer.send_message(common.channels['iq']['zac-testing'], msg)

    def trigger_random(self):
        tree = ET.parse(os.path.join('./resources', 'random_comments.xml'))
        root = tree.getroot()
        txt = root[int(random.random()*len(root))].text
        try:
            self.msg_writer.send_message('C15S4357W', txt)
        except:
            self.msg_writer.send_message('C15S5LNM9', txt)
        self.trigger_method_log('random')

    def check_trigger_random(self, hour, minute):
        random_should_fire_hr = (self.last_random_hour + int(self.random_interval_minutes/MIN_PER_HOUR) + int((self.last_random_minutes + self.random_interval_minutes%MIN_PER_HOUR)/MIN_PER_HOUR))%HR_PER_DAY
        random_should_fire_min = (self.last_random_minutes + self.random_interval_minutes%MIN_PER_HOUR)%MIN_PER_HOUR #math
        if self.random_hasnt_fired or (hour == random_should_fire_hr and minute == random_should_fire_min):
            max_minutes_between_random_events = 720 #24 hours max
            new_random_minutes = int(random.random()*max_minutes_between_random_events) + 1
            if hour >= 14 and hour < 18 and self.random_hasnt_fired == False:
                self.trigger_random()
            self.last_random_hour = hour
            self.last_random_minutes = minute
            self.random_interval_minutes = new_random_minutes
            if self.random_hasnt_fired:
                #self.clients.upload_file_to_slack() #test file upload
                #self.clients.get_file_info()
                self.random_hasnt_fired = False

    def trigger_wine_club(self):
        tag_users = ['channel', 'here']
        msg = 'WINE CLUB IN THE LOUNGE :wine_glass: :wine_glass: :wine_glass: :wine_glass: :wine_glass:'
        txt = '<!{}> {}'.format(random.choice(tag_users), msg)
        self.msg_writer.send_message('C15S4357W', txt)

    def trigger_drunk_phrase(self):
        channel = 'C15S4357W'
        random_custom_emoji = self.clients.get_random_emoji()
        drunk_comments_file = open(os.path.join('./resources', 'drunk_comments.txt'), 'r')
        drunk_comments = drunk_comments_file.read().splitlines()
        txt = '{} :{}:'.format(random.choice(drunk_comments), random_custom_emoji)
        self.msg_writer.send_message(channel, txt)

    def trigger_weather(self):
        response = weather_manager.getCurrentWeather()
        # response = WeatherController.get_weather()
        try:
            self.msg_writer.send_message(common.channels['slackers']['zac-testing'], response)
        except:
            self.msg_writer.send_message(common.channels['iq']['zac-testing'], response)

    def trigger_945(self):
        random_custom_emoji = self.clients.get_random_emoji()
        tag_users = ['channel', 'here']
        kip_msgs = ['@945', '945!', '#945', ':paw_prints: 945!', '~945~', ':horse: 945! giddyup', '945! :heart:', '945! :sweet_potato:', '945!........', '945 time', '945 quickie', '945 o\'clock', '945! :sheep: :panda_face: :slowpoke:', '945! :boom:', ':eggplant: 945.', '945 :coffee:', '_le 945_', '_le fast 945_']
        txt = '<!{}> {} :{}:'.format(random.choice(tag_users), random.choice(kip_msgs), random_custom_emoji)
        try:
            self.msg_writer.send_message('C15S4357W', txt)
        except:
            self.msg_writer.send_message('C15S5LNM9', txt)

    def trigger_mochaccino(self):
        tag_users = ['channel', 'here']
        msgs = ['The mochaccino tastes _amazing_ this morning!', 'Eh, mochaccino ain\'t so great today...', 'HELP! MOCHACCINO EVERYWHERE!',
        'The mochaccino machine won\'t stop dripping help I need an adult', 'WHAT! wHY is my mochaccino _decaf_??!', 'I haven\'t had my mochaccino yet don\'t talk to me',
        'WHERE\'S MY MUG I NEED MOCHACCINO!!', 'Mochaccino mochaccino mochaccino', 'Mochaccino is SO GOOD TODAY HOLY HELL',
        'Today\'s mochaccino is like an angel pooped out a nice hot cup of coffee mmmmm~', 'Mochaccino status: passable',
        'MOCHACCINO MOCHACCINO MOCHACCINO!!!', 'Who\'s ready for a nice cup o\' mochaccino?', '_le mochaccino_']
        txt = '<!{}> {} :coffee:'.format(random.choice(tag_users), random.choice(msgs))
        try:
            self.msg_writer.send_message('C15S4357W', txt)
        except:
            self.msg_writer.send_message('C15S5LNM9', txt)

    def trigger_timed_event(self):
        #get date and time
        curr_datetime = datetime.utcnow() - timedelta(hours=HOUR_DIFFERENCE_DAYLIGHT_SAVINGS) #change here when daylight savings ends
        day = curr_datetime.strftime('%A')
        hour = int(curr_datetime.strftime('%H'))
        minute = int(curr_datetime.strftime('%M'))
        second = int(curr_datetime.strftime('%S'))

        #trigger startup log to testing channel
        if(self.is_just_starting_up):
            self.trigger_startup_log(day, hour, minute, second)
            self.is_just_starting_up = False

        #leaves 10-ish seconds to trigger since method is called every 10-ish seconds and we wantz the if statement to trigger once per min only
        if(second >= 5 and second <= 15):
            #self.trigger_ping(day, hour, minute, second) #will post a ping every minute to testing channel
            self.check_trigger_random(hour, minute)
            if hour % 3 == 0 and minute == 0:
                self.trigger_weather()
            if minute == 15:
                self.trigger_markov()
            if day != 'Saturday' and day != 'Sunday' and hour == 9 and minute == 45:
                self.trigger_945()
            if day != 'Saturday' and day != 'Sunday' and hour == 9 and minute == 0:
                self.trigger_mochaccino()
            if day == 'Friday':
                if hour == 16 and minute == 30:
                    self.trigger_wine_club()
                if (hour == 16 and minute == 35) or (hour == 17 and minute == 0) or (hour == 17 and minute == 30) or (hour == 18 and minute == 0):
                    self.trigger_drunk_phrase()
