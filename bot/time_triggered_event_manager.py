import random
from datetime import datetime, timedelta

HOUR_DIFFERENCE_DAYLIGHT_SAVINGS = 5 #for Winnipeg
HOUR_DIFFERENCE_NO_DAYLIGHT_SAVINGS = 6 #for Winnipeg

class TimeTriggeredEventManager(object):

    def __init__(self, slack_clients):
        self.clients = slack_clients

        def trigger_timed_event(self):
            curr_datetime = datetime.utcnow() - timedelta(hours=HOUR_DIFFERENCE_DAYLIGHT_SAVINGS) #change here when daylight savings ends
            day = curr_datetime.strftime('%A')
            hour = int(curr_datetime.strftime('%H'))
            minute = int(curr_datetime.strftime('%M'))
            second = int(curr_datetime.strftime('%S'))
            if(second >= 5 and second <= 15):
                msg = 'this is a test message at hour: ' + str(hour)  + ' and minute: ' + str(minute) + ' and second: ' + str(second) + ' and day: ' + day
                self.clients.send_time_triggered_msg('#zacefron-testing', msg)
                #if(hour == 9 and minute == 45)
                    #kip_msgs = ['@945', '945!', 'Guten Morgen', 'Bonjour', 'Ohayou', 'Good morning to you', 'Aloha', 'Konnichiwashington', 'Buenos dias', ':sunny: Good morning']
                    #txt = '<@channel> {}'.format(random.choice(good_mornings), user_id)dle