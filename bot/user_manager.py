import json

class UserManager:
	
	def __init__(self, clients, msg_writer):
		self.clients = clients
		self.users = self.clients.api_call("users.list")
		self.users = json.dumps(self.users)
		self.users = json.loads(str(self.users))
		msg_writer.write_custom_error(self.users)
		self.user_names = dict()
		for user in self.users:
			self.user_names[user["id"]] = user["name"]

	def get_user(self, key):
		if key in self.user_names:
			return self.user_names[key]
		return None
		