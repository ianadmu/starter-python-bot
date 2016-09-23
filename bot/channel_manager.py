import json


class ChannelManager:

    def __init__(self, slack_clients):
        self.clients = slack_clients
        channels = self.clients.get_channels()
        self.channel_names = {}
        self.channel_ids = {}
        if channels["ok"]:
            for channel in channels["channels"]:
                self.channel_names[channel["id"]] = channel["name"]
                self.channel_ids[channel["name"]] = channel["id"]

    def get_channel_id(self, identifier):
        if identifier in self.channel_ids:
            return identifier
        elif identifier in self.channel_names:
            return channel_ids[identifier]
        else:
            return None

    def get_channel_by_id(self, channel_id):
        if channel_id in self.channel_names:
            return self.channel_names[channel_id]
        return None

    def get_channel_by_name(self, name):
        if name in self.channel_ids:
            return self.channel_ids[name]
        return None
