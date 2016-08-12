class Game:

	def __init__(self, game, players):
		self.game = game
		self.players = dict()
		for player_num in range(len(players)):
			self.players[players[player_num]] = player_num

	def process_command(self, message, player):
		return self.game.process_command(message, self.players[player])

class GameManager:

	def __init__(self, msg_writer):
		self.games = dict()
		self.msg_writer = msg_writer

	def _make_key(self, players, channel, game_name):
		return frozenset(channel, frozenset(players), game_name)

	def add_game(self, game, players, channel, game_name):
		#game should be initialized here
		key = self._make_key(players, channel, game_name)
		self.games[key] = Game(game, players)
		self.msg_writer.send_message(channel, str(game))

	def process_message(self, players, channel, game_name, message, current_player):
		#the message needs to be parsed earlier up in the process
		#this is making no assumptions about what information the game needs
		key = self._make_key(players, channel, game_name)
		if key in self.games:
			game = self.games[key]
			result = game.process_command(message, current_player)
			self.msg_writer.send_message(channel, result)
		else:
			error_msg = "There is currently no game that can be selected with the information provided"
			self.msg_writer(channel, error_msg)


