import logging
import random
from datetime import datetime
from loud_manager import LoudManager
from hogwarts_house_sorter import HogwartsHouseSorter
import scripts.weather_controller
from scripts.weather_controller import WeatherController
from sass_manager import SassManager
from apology_manager import ApologyManager
from equation_manager import EquationManager

logger = logging.getLogger(__name__)
class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.loud_manager = LoudManager()
        self.hogwarts_house_sorter = HogwartsHouseSorter()
        self.sass_manager = SassManager()
        self.apology_manager = ApologyManager()
        self.equation_manager = EquationManager()

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}'.format(
            "I'm Zac Efron.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll greet back, i don't bite. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> weather` - Let me tell you the weather in Winnipeg. :rainbow:",
            "> `<@" + bot_uid + "> I'm sad` - Maybe I can cheer you up. :wink: ",
            "> Don't mind this message! :camel:")
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_your_welcome(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        your_welcomes = ['No problem mon', 'Please don\'t use Comic Sans; this isn\'t a lemonade stand', 'Why, you\'re welcome my friend', 'Don\'t mention it', 'Don\'t mention it', 'You\'re welcome', 'It was a pleasure', 'It was my pleasure', 'No sweat', 'Anytime', '_Le gratitude_ pleases me. :heart: Thank you', 'No worries', 'No, thank you']
        txt = '{}, <@{}>!'.format(random.choice(your_welcomes), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)

    def announce_945(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        time1 = datetime.now()
        time2 = datetime.time(9,45,0)
        time3 = time1 - time2
        self.send_message(channel_id, time1.__str__() +" "+ time2.__str__() + " "+ time3.__str__())
        self.send_message(channel_id,"945 :sunny: time now is " + datetime.now().strftime('%H:%M'))
        self.send_message(channel_id,"/digg editions")

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def write_sad(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        txt = "This always cracks me up. :wink:"
        self.send_message(channel_id, txt)
        self.clients.send_user_typing_pause(channel_id)
        attachment = {
            "title": "/giphy bloopin",
            "title_link": "http://giphy.com/gifs/friday-rebecca-black-hurrr-13FsSYo3fzfT2g",
            "image_url": "http://i.giphy.com/13FsSYo3fzfT2g.gif",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id,"", attachments=[attachment], as_user='true')
        txt = "I'm crying into my tea. :joy:"
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
    
    def write_weather(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        response = WeatherController.get_weather()
        self.send_message(channel_id, response)

    def write_loud(self,channel_id,origMessage):
        self.loud_manager.write_loud_to_file(origMessage)
        self.send_message(channel_id, self.loud_manager.get_random_loud())

    def write_hogwarts_house(self, channel_id, user_id, msg):
        self.clients.send_user_typing_pause(channel_id)
        response = self.hogwarts_house_sorter.sort_into_house(msg)
        txt = '<@{}>: {}'.format(user_id, response)
        self.send_message(channel_id, txt)

    def write_sass(self, channel_id, msg):
        self.clients.send_user_typing_pause(channel_id)
        txt = self.sass_manager.get_sass(msg)
        self.send_message(channel_id, txt)
        
    def write_apology(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, self.apology_manager.get_random_apology())

    def write_test(self):
        self.send_message('zacefron-dev', 'This is a test time triggered event')
        self.clients.api_call('chat.postMessage', as_user='true:', channel='zacefron-dev', text='helloooooooooooo')
        #self.clients.send_user_typing_pause(channel_id)
        #self.send_message(channel_id, 'This is a test time triggered event')

    def write_solution(self,channel_id, msg):
        self.send_message(channel_id, self.equation_manager.solve(msg))
        
