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
        groups = self.clients.get_groups()
        if groups["ok"]:
            for group in groups["groups"]:
                self.channel_names[group["id"]] = group["name"]
                self.channel_ids[group["name"]] = group["id"]
        self.load_ims()

    def get_channel_id(self, identifier):
        self.load_ims()
        if identifier in self.channel_ids:
            return self.channel_ids[identifier]
        elif identifier in self.channel_names:
            return identifier
        elif identifier.replace('#', '') in self.channel_ids:
            return self.channel_ids[identifier.replace('#', '')]
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

    def load_ims(self):
        ims = self.clients.get_ims()
        if ims["ok"]:
            for im in ims["ims"]:
                self.channel_names[im["id"]] = im["user"]  # user = user_id
                self.channel_ids[im["user"]] = im["id"]
