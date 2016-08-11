import json

class UserManager:
	
	def __init__(self, clients, msg_writer):
		msg_writer.write_custom_error("Starting to load")
		self.users = clients.get_users()
		msg_writer.write_custom_error("Api call")
		self.users = json.dumps(self.users)
		msg_writer.write_custom_error("Dumps")
		msg_writer.write_custom_error(str(self.users))
		self.users = json.loads(str(self.users))
		msg_writer.write_custom_error("Loads")
		self.user_names = dict()
		if self.users["ok"]:
			msg_writer.write_custom_error("Is ok")
			for user in self.users["members"]:
				self.user_names[user["id"]] = user["name"]
		else:
			msg_writer.write_custom_error("Is not ok")
			if "error" in self.users:
				msg_writer.write_custom_error(self.users["error"])
			else:
				msg_writer.write_custom_error("Something bad happend while loading users")

	def get_user(self, key):
		if key in self.user_names:
			return self.user_names[key]
		return None
		