import json

class UserManager:
	
	def __init__(self, clients, msg_writer):
		self.users = clients.get_users()
		self.user_names = dict()
		self.user_ids = dict()
		if self.users["ok"]:
			for user in self.users["members"]:
				self.user_names[user["id"]] = user["name"]
				self.user_ids[user["name"]] = user["id"]
		else:
			if "error" in self.users:
				msg_writer.write_custom_error(self.users["error"])

	def print_all_users(self, msg_writer):
		for name, user_id in self.user_ids:
			msg_writer.write_custom_error(name + ": " + user_id)

	def get_user_by_id(self, user_id):
		if user_id in self.user_names:
			return self.user_names[user_id]
		return None

	def get_user_by_name(self, name):
		if name in self.user_names:
			return self.user_names[name]
		return None

	def get_users_mentioned(self, message):
		mentioned_users = set()
		for token in message.split():
			if token in self.user_ids:
				mentioned_users.add(token)
		return mentioned_users

		