import json

class ChannelManager:
	
	def __init__(self, clients):
		channels = clients.get_channels()
		self.channel_names = dict()
		self.channel_ids = dict()
		if self.channels["ok"]:
			for channel in channels["channels"]:
				self.channel_names[channel["id"]] = channel["name"]
				self.channel_ids[channel["name"]] = channel["id"]

	def get_channel_id(self, identifier):
		if identifier in self.channel_names:
			return self.channel_names[identifier]
		elif identifier in self.channel_ids:
			return identifier
		else
			return None

	def get_channel_by_id(self, user_id):
		if channel_id in self.channel_names:
			return self.channel_names[channel_id]
		return None

	def get_channel_by_name(self, name):
		if name in self.channel_ids:
			return self.channel_ids[name]
		return None