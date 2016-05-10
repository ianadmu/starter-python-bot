import random
import json
from datetime import datetime, timedelta

HOUR_DIFFERENCE_DAYLIGHT_SAVINGS = 5 #for Winnipeg
HOUR_DIFFERENCE_NO_DAYLIGHT_SAVINGS = 6 #for Winnipeg

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

    def trigger_random(self, last_random, random_interval, new_random, hr, min):
        #channels = ['heliwolves', 'spamalot']
        #channel = '#{}'.format(random.choice(channels)) 
        random_msgs = ['Steven is a wiener :eggplant:', 'this is a random message', 'this is random message number 2', 'random message number 3']
        msg = 'Last random minute: {} and last random interval: {} and new random interval: {} and Message: {} comapre hr: {} and compare min:{}'.format(last_random, random_interval, new_random, random.choice(random_msgs), hr, min)
        self.clients.send_time_triggered_msg('#zacefron-testing', msg)

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
        if(second >= 5 and second <= 15):
            #self.trigger_ping(day, hour, minute, second)
            hr = self.last_random_hour + int(self.random_interval_minutes/60) + int((self.last_random_minutes + self.random_interval_minutes%60)/60)%24
            min = (self.last_random_minutes + self.random_interval_minutes%60)%60
            if self.random_hasnt_fired or (hour == hr and minute == min): 
                new_random = int(random.random()*5) + 1 #fire at least every 5 minutes
                #if hour > 8 and hour < 22: #ping and random event fire for testing
                self.trigger_ping(day, hour, minute, second)
                self.trigger_random(self.last_random_minutes, self.random_interval_minutes, new_random, hr, min)
                self.random_interval_minutes = new_random
                self.last_random_minutes = minute
                self.last_random_hour = hour
                if self.random_hasnt_fired:
                    self.random_hasnt_fired = False
            if hour == 9 and minute == 45:
                self.trigger_945()

