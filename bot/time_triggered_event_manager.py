import random
import json
import os.path
import xml.etree.ElementTree as ET 
from datetime import datetime, timedelta

HOUR_DIFFERENCE_DAYLIGHT_SAVINGS = 5 #for Winnipeg
HOUR_DIFFERENCE_NO_DAYLIGHT_SAVINGS = 6 #for Winnipeg
MIN_PER_HOUR = 60
HR_PER_DAY = 24

class TimeTriggeredEventManager(object):

    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.last_random_hour = 0
        self.last_random_minutes = 0
        self.random_interval_minutes = 0
        self.random_hasnt_fired = True

    def trigger_ping(self, day, hour, minute, second):
        random_custom_emoji = self.clients.get_random_emoji()
        msg = 'Ping on ' + day + ' ' + str(hour)  + ':' + str(minute) + ':' + str(second) + ' :' + str(random_custom_emoji) + ':' 
        self.clients.send_time_triggered_msg('#zacefron-testing', msg)

    def trigger_random(self, new_random_minutes):
        #channels = ['heliwolves', 'spamalot']
        #channel = '#{}'.format(random.choice(channels)) 
        tree = ET.parse(os.path.join('./resources', 'random_comments.xml'))
        root = tree.getroot()
        txt = root[int(random.random()*len(root))].text
        msg = 'New random interval in minutes: {} with message: {} '.format(new_random_minutes, txt)
        self.clients.send_time_triggered_msg('#zacefron-testing', msg)

    def check_trigger_random(self, day, hour, minute, second):
        random_should_fire_hr = (self.last_random_hour + int(self.random_interval_minutes/MIN_PER_HOUR) + int((self.last_random_minutes + self.random_interval_minutes%MIN_PER_HOUR)/MIN_PER_HOUR))%HR_PER_DAY
        random_should_fire_min = (self.last_random_minutes + self.random_interval_minutes%MIN_PER_HOUR)%MIN_PER_HOUR #math
        if self.random_hasnt_fired or (hour == random_should_fire_hr and minute == random_should_fire_min): 
            new_random_minutes = int(random.random()*174) + 1 #fire at least every 5 minutes
            #if hour > 8 and hour < 22: #ping and random event fire for testing #when done testing uncomment and indent the next 2 lines when you uncomment!!!!
            self.trigger_ping(day, hour, minute, second)
            self.trigger_random(new_random_minutes)
            self.random_interval_minutes = new_random_minutes
            self.last_random_minutes = minute
            self.last_random_hour = hour
            if self.random_hasnt_fired:
                #self.clients.upload_file_to_slack() #test file upload
                self.random_hasnt_fired = False

    def trigger_945(self):
        random_custom_emoji = self.clients.get_random_emoji()
        tag_users = ['channel', 'here']
        kip_msgs = ['@945', '945!', '#945', ':paw_prints: 945!', '~945~', ':horse: 945! giddyup', '945! :heart:', '945! :sweet_potato:', '945!........', '945 time', '945 quickie', '945 o\'clock', '945! :sheep: :panda_face: :slowpoke:', '945! :boom:', ':eggplant: 945.', '945 :coffee:', '_le 945_', '_le fast 945_']
        txt = '<!{}> {} :{}:'.format(random.choice(tag_users), random.choice(kip_msgs), random_custom_emoji) #<!channel> instead of using @
        self.clients.send_time_triggered_msg('#random', txt)

    def trigger_timed_event(self):
        curr_datetime = datetime.utcnow() - timedelta(hours=HOUR_DIFFERENCE_DAYLIGHT_SAVINGS) #change here when daylight savings ends
        day = curr_datetime.strftime('%A')
        hour = int(curr_datetime.strftime('%H'))
        minute = int(curr_datetime.strftime('%M'))
        second = int(curr_datetime.strftime('%S'))
        if(second >= 5 and second <= 15): #leave a bit over 10 seconds to trigger, method is called every 10-ish s and we only want it to trigger once per min
            #self.trigger_ping(day, hour, minute, second)
            self.check_trigger_random(day, hour, minute, second) #in own method because math
            if hour == 9 and minute == 45:
                self.trigger_945()
