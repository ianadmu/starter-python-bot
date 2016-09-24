import random
import json
import os.path
import re


class Response:

    names = ["zac", "qbot"]

    def __init__(
        self, phrases, words, emoji, responses,
        use_hash, named, start, end, sender
    ):
        self.phrases = phrases
        self.words = words
        self.responses = responses
        self.use_hash = use_hash
        self.named = named
        self.start = start
        self.end = end
        self.emoji = emoji
        self.sender = sender

    def get_emoji_response(self, reaction):
        if reaction in self.emoji:
            return self.random()
        return ""

    def get_response(self, message, tokens, user):
        has_trigger = False
        is_named = False
        lower = message.lower()
        for phrase in self.phrases:
            if phrase in lower:
                has_trigger = True
                continue

        if not has_trigger:
            for word in self.words:
                for token in tokens:
                    if word == token:
                        has_trigger = True
                        continue

        for name in Response.names:
            if name in lower:
                is_named = True

        result = ""

        if has_trigger and (not self.named or is_named):
            if self.use_hash:
                result = self.hash(message)
            else:
                result = self.random()
        result = result.replace("user_id", "<@" + user + ">")
        return result

    def hash(self, text):
        hashValue = 11
        for character in text:
            hashValue *= 47
            hashValue += ord(character)
        return self.start + self.responses[hashValue % len(self.responses)] + self.end

    def random(self):
        return self.start + random.choice(self.responses) + self.end


class Response_master:
    string_split = "[\s\.,?!]"

    def __init__(self, msg_writer):
        try:
            master_file = open(os.path.join('./resources', 'events.txt'), 'r')
            json_events = json.load(master_file)
            self.events = []
            for event in json_events["Events"]:
                use_hash = "Hash" in event and event["Hash"]
                named = "Named" in event and event["Named"]
                start = ""
                end = ""
                sender = ""
                if "Start" in event:
                    start = event["Start"]
                if "End" in event:
                    end = event["End"]
                if "Sender" in event:
                    sender = event["Sender"]
                phrases = []
                words = []
                emoji = []
                responses = []
                if "Words" in event["Triggers"]:
                    for w in event["Triggers"]["Words"]:
                        words.append(w)
                if "Phrases" in event["Triggers"]:
                    for p in event["Triggers"]["Phrases"]:
                        phrases.append(p)
                if "Emoji" in event["Triggers"]:
                    for e in event["Triggers"]["Emoji"]:
                        emoji.append(e)
                for r in event["Responses"]:
                    responses.append(r)
                self.events.append(
                    Response(
                        phrases, words, emoji, responses,
                        use_hash, named, start, end, sender
                    )
                )
                self.msg_writer = msg_writer
        except:
            msg_writer.write_custom_error("Error loading JSON file")
            self.events = []

    def get_emoji_response(self, response):
        combined_responses = ""
        for event in self.events:
            current_response = event.get_emoji_response(response)
            if current_response != "":
                current_response += '\n'
            combined_responses += current_response

        return combined_responses

    def give_message(self, channel, message, user):
        combined_responses = ""
        tokens = re.split(self.string_split, message.lower())
        sender = None
        for event in self.events:
            current_response = event.get_response(message, tokens, user)
            if current_response != "":
                current_response += '\n'
                if event.sender:
                    sender = event.sender
            combined_responses += current_response

        if sender:
            self.msg_writer.send_message_as_other(
                channel, combined_responses, sender, ':' + sender + ':'
            )
        else:
            self.msg_writer.send_message(channel, combined_responses)
        return combined_responses
