import json

class UserManager:
	
	def __init__(self, clients):
		self.clients = clients
		self.users = self.clients.api_call("users.list")
		self.users = json.dumps(self.users)
		self.users = json.loads(str(self.users))
		if self.users["ok"]:
			self.user_names = dict()
			for user in self.users["members"]:
				self.user_names[user["id"]] = user["name"]

	def get_user(self, key):
		if key in self.user_names:
			return self.user_names[key]
		return None
		