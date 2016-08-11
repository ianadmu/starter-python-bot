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

	def get_user_by_id(self, user_id):
		if user_id in self.user_names:
			return self.user_names[user_id]
		return None

	def get_user_by_name(self, name):
		if name in self.user_names:
			return self.user_names[name]
		return None
		