import random
import json
import os.path

class Response:

	name = "zac"

	def __init__(self, triggers, responses, use_hash, named):
		self.triggers = triggers
		self.responses = responses
		self.use_hash = use_hash
		self.named = named

	def get_response(self, message, user):
		has_trigger = False
		lower = message.lower()
		for trigger in self.triggers:
			if trigger in lower:
				has_trigger = True

		result = ""

		if has_trigger and (not self.named or Response.name in lower):
			if self.use_hash:
				result = self.hash(message)
			else:
				result = self.random()
		result = result.replace("user_id", "<@" + user + ">")
		return result

	def hash(self, text):
		hashValue = 11;
		for character in text:
			hashValue *= 47
			hashValue += ord(character)
		return self.responses[hashValue % len(self.responses)]

	def random(self):
		return random.choice(self.responses)

class Response_master:

	def __init__(self, msg_writer):
		try:
			master_file = open(os.path.join('./resources', 'events.txt'), 'r')
			json_events = json.load(master_file)
			self.events = []
			for event in json_events["Events"]:
				use_hash = ("Hash" not in event) or event["Hash"]
				named = "Named" in event and event["Named"]
				triggers = []
				responses = []
				for t in event["Triggers"]:
					triggers.append(t)
				for r in event["Responses"]:
					responses.append(r)
				self.events.append(Response(triggers, responses, use_hash, named))
		except :
			msg_writer.write_error("Error loading JSON file")
			self.events = []

	def get_response(self, message, user):
		combined_responses = ""
		for event in self.events:
			current_response = event.get_response(message, user)
			if current_response != "":
				current_response += '\n'
			combined_responses += current_response

		return combined_responses