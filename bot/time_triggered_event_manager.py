import random
import json
from datetime import datetime, timedelta

HOUR_DIFFERENCE_DAYLIGHT_SAVINGS = 5 #for Winnipeg
HOUR_DIFFERENCE_NO_DAYLIGHT_SAVINGS = 6 #for Winnipeg

class TimeTriggeredEventManager(object):

    def __init__(self, slack_clients):
        self.clients = slack_clients

    def trigger_ping(self, day, hour, minute, second):
        random_custom_emoji = self.clients.get_random_emoji()
        msg = 'Ping on ' + day + ' ' + str(hour)  + ':' + str(minute) + ':' + str(second) + ' :' + str(random_custom_emoji) + ':' 
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
        if(hour > 11 and hour < 18 and second >= 5 and second <= 15):
            self.trigger_ping(day, hour, minute, second)
            if hour == 9 and minute == 45:
                self.trigger_945()

