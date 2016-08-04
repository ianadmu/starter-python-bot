import random
import json
import os.path

class Response:

	def __init__(self, triggers, responses, use_hash):
		self.triggers = triggers
		self.responses = responses
		self.use_hash = use_hash

	def get_response(self, message):
		has_trigger = False
		lower = message.lower()
		for trigger in self.triggers:
			if trigger in lower:
				has_trigger = True

		if has_trigger:
			if self.use_hash:
				return self.hash(message)
			else:
				return self.random()
		return ""

	def hash(self, text):
		hashValue = 11;
		for character in text:
			hashValue *= 47
			hashValue += ord(character)
		return self.responses[hashValue % len(self.responses)]

	def random(self):
		return random.choice(self.responses)

class Response_master:

	def __init__(self):
		master_file = open(os.path.join('./resources', 'events.txt'), 'r')
		json_events = json.load(master_file)
		self.events = []
		for event in json_events["Events"]:
			use_hash = (not "Hash" in event) or event["Hash"]
			triggers = []
			responses = []
			for t in event["Triggers"]:
				triggers.append(t)
			for r in event["Responses"]:
				responses.append(r)
			self.events.append(Response(triggers, responses, use_hash))

	def get_response(self, message):
		combined_responses = ""
		for event in self.events:
			combined_responses += event.get_response(message)

		return combined_responses