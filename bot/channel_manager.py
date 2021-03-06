class ChannelManager:
    banned_channels = ["events", "games", "tautology", "work"]

    def __init__(self, slack_clients):
        self.clients = slack_clients
        channels = self.clients.get_channels()
        groups = self.clients.get_groups()
        ims = self.clients.get_ims()
        self.channel_names = {}
        self.channel_ids = {}
        if channels['ok']:
            for channel in channels['channels']:
                if channel['name'] not in ChannelManager.banned_channels:
                    self.channel_names[channel['id']] = channel['name']
                    self.channel_ids[channel['name']] = channel['id']

        if groups['ok']:
            for group in groups['groups']:
                self.channel_names[group['id']] = group['name']
                self.channel_names[group['name']] = group['id']

        if ims['ok']:
            for im in ims['ims']:
                self.channel_names[im['id']] = im['user']
                self.channel_names[im['user']] = im['id']

    def get_channel_id(self, identifier):
        identifier = identifier.replace('#', '')
        if identifier in self.channel_ids:
            return self.channel_ids[identifier]
        elif identifier in self.channel_names:
            return identifier
        elif isinstance(identifier, dict):
            return identifier['id']
        else:
            return self.channel_ids['zac-testing']

    def get_channel_by_id(self, channel_id):
        if channel_id in self.channel_names:
            return self.channel_names[channel_id]
        return None

    def get_channel_by_name(self, name):
        if name in self.channel_ids:
            return self.channel_ids[name]
        return None

    def get_all_channel_ids(self):
        # return a copy of all channel ids
        return list(self.channel_ids.values())

    def get_all_channel_names(self):
        # return a copy of all channel names
        return list(self.channel_names.values())
