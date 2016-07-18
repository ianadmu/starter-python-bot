import json
import logging
import re

logger = logging.getLogger(__name__)

class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def is_loud(self,message):
        emoji_pattern = re.compile(":.*:")
        tag_pattern = re.compile("<@.*")
        tokens = message.split()

        if len(tokens) < 2: 
            return False
        for token in message.split():
            if not (token.isupper() or emoji_pattern.match(token)) or tag_pattern.match(token):
                return False

        return True

    def _handle_message(self, event):
        if 'subtype' in event:
            if event['subtype'] == 'message_changed':
                self.msg_writer.write_spelling_mistake(event['channel'])
            elif event['subtype'] == 'channel_join':
                # someone joined a channel
                self.msg_writer.write_joined_channel(event['channel'], event['user'])
            elif event['subtype'] == 'message_deleted':
                self.msg_writer.write_message_deleted(event['channel'])
            elif event['subtype'] == 'channel_leave':
                self.msg_writer.write_left_channel(event['channel'])

        # Filter out messages from the bot itself
        if 'user' in event and not self.clients.is_message_from_me(event['user']):

            msg_txt = event['text']
            channel = event['channel']
            user = event['user']

            if re.search('qbot', msg_txt.lower()):
                self.msg_writer.write_no_qbot(channel)

            if self.is_loud(msg_txt):
                self.msg_writer.write_loud(channel, msg_txt)

            if re.search('i choose you', msg_txt.lower()):
                self.msg_writer.write_cast_pokemon(channel, msg_txt.lower())

            if re.search('cry|crying', msg_txt.lower()):
                self.msg_writer.write_crying_into_my_tea(channel)

            if 'wiener' in msg_txt.lower():
                self.msg_writer.write_wiener(channel)

            if re.search('boyer', msg_txt.lower()):
                self.msg_writer.write_boyer_bot(channel)

            if re.search('weather', msg_txt.lower()):
                self.msg_writer.write_weather(channel)

            if msg_txt.endswith('*'):
                self.msg_writer.write_spelling_mistake(channel)

            if re.search('fuck this', msg_txt.lower()):
                self.msg_writer.write_fuck_this(channel)
                
            if re.search('just do it', msg_txt.lower()):
                self.msg_writer.write_do_it(channel)
                
            if re.search(' ?zac', msg_txt.lower()) or self.clients.is_bot_mention(msg_txt) or re.search('qbot', msg_txt.lower()):
                if 'help' in msg_txt.lower():
                    self.msg_writer.write_help_message(channel)
                if re.search('hi |hey|hello|howdy|sup ', msg_txt.lower()) or msg_txt.lower().endswith(' hi') or msg_txt.lower().endswith(' sup'):
                    self.msg_writer.write_greeting(channel, user)
                if re.search('morning', msg_txt.lower()):
                    self.msg_writer.write_good_morning(channel, user)
                if re.search('night', msg_txt.lower()):
                    self.msg_writer.write_good_night(channel, user)
                if re.search('thanks|thank you|thank-you', msg_txt.lower()):
                    self.msg_writer.write_your_welcome(channel, user)
                if 'joke' in msg_txt.lower():
                    self.msg_writer.write_joke(channel)
                if 'french' in msg_txt.lower():
                    self.msg_writer.write_to_french(channel, msg_txt)
                if re.search('who\'?s that pokemon', msg_txt):
                    self.msg_writer.write_whos_that_pokemon(channel)
                if re.search(' ?zac it\'?s', msg_txt.lower()):
                    self.msg_writer.write_pokemon_guessed_response(channel, user, msg_txt)
                if 'attachment' in msg_txt:
                    self.msg_writer.demo_attachment(channel)
                if 'sad' in msg_txt.lower():
                    self.msg_writer.write_sad(channel)
                if 'kill me' in msg_txt.lower():
                    self.msg_writer.write_bang(channel, user)
                if re.search('(feed)|(hungry)', msg_txt.lower()):
                    self.msg_writer.write_food(channel)
                if re.search('encourage me', msg_txt.lower()):
                    self.msg_writer.write_encouragement(channel, user)
                if 'sort me' in msg_txt.lower():
                    self.msg_writer.write_hogwarts_house(channel, user,  msg_txt)
                if 'sass ' in msg_txt.lower():
                    self.msg_writer.write_sass(channel, msg_txt)	
                if re.search('apologize|apologise', msg_txt.lower()):
                    self.msg_writer.write_apology(channel)
                if 'solve' in msg_txt.lower():
                    self.msg_writer.write_solution(channel, msg_txt)
                if  re.search('explain|why', msg_txt.lower()):
                    self.msg_writer.write_explanation(channel)
                if re.search('sweetpotato me|sweet potato me', msg_txt.lower()):
                    self.msg_writer.write_sweetpotato_me(channel, user)
                if re.search('marry me', msg_txt.lower()):
                    self.msg_writer.write_marry_me(channel)
                if re.search('draw me', msg_txt.lower()):
                    self.msg_writer.write_draw_me(channel)
                if re.search('love|forever|relationship|commitment', msg_txt.lower()):
                    self.msg_writer.write_forever(channel)
                if re.search('story|stories', msg_txt.lower()):
                    self.msg_writer.write_story(channel)
                if re.search('unflip',msg_txt.lower()):
                    self.msg_writer.write_unflip(channel)
                elif re.search('flip|rageflip',msg_txt.lower()):
                    self.msg_writer.write_flip(channel)
                if re.search('sup son',msg_txt.lower()):
                    self.msg_writer.write_sup_son(channel)
                else:
                    pass
