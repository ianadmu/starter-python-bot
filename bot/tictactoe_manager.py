from tictactoe import TicTacToe
from collections import defaultdict

class TicTacToeManager:
	help_message = "To talk to the TicTacToe manager type a sentence that starts with 'tictactoe' or 'ttt'\n"
	help_message += "To start a game agaisnt Zac, type start as the second word, followed by the size of the square board, and the length required to win\n"
	help_message += "To play a move, type where you would like to go as the second word\n"
	help_message += "To have Zac play himself, type self instead of start"

	def __init__(self, msg_writer):
		self.games = defaultdict(lambda: TicTacToe(3,3, True))
		self.msg_writer = msg_writer

	def get_message(self, channel, message):
		command = message.split()
		if len(command) > 3:
			if command[1].upper() == "START":
				try:
					size = int(command[2])
					length = int(command[3])
					self.start(channel, size, length)
				except:
					self.msg_writer.send_message(channel,"Error parsing initial prameters")
			elif command[1].upper() == "SELF":
				try:
					size = int(command[2])
					length = int(command[3])
					self.play_self(channel, size, length)
				except:
					self.msg_writer.send_message(channel,"Error parsing initial prameters")

		elif len(command) > 1:
			if command[1].upper() == "HELP":
				self.msg_writer.send_message(channel,TicTacToeManager.help_message)
			else:
				self.process_command(channel, command[1])

	def play_self(self, channel, size, length):
		self.games[channel] = TicTacToe(size, length, True)
		self.msg_writer.send_message(channel,self.games[channel].play_self())

	def start(self, channel, size, length):
		self.games[channel] = TicTacToe(size, length, True)
		self.msg_writer.send_message(channel,self.games[channel].__str__())

	def process_command(self, channel, command):
		result = self.games[channel].process_command(command)
		self.msg_writer.send_message(channel,result)
