import random
import json
import os

class Response:

	def __init__(self, triggers, responses, use_hash):
		self.triggers = triggers
		self.responses = responses
		self.use_hash = use_hash

	def get_response(self, message):
		has_trigger = False
		for trigger in self.triggers:
			if trigger in message:
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
		json_events = json.load(master_file.read())
		self.responses = []
		for event in json_events["Events"]:
			use_hash = not "Hash" in event or event["Hash"]
			self.responses.append(Response(event["Triggers"], event["Responses"],use_hash))

	def get_response(self, message):
		combined_responses = ""
		for responses in self.responses:
			combined_responses += responses.get_response(message)

		return combined_responses

res = Response_master()
print(res.get_response("!@#$"))





