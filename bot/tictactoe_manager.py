from tictactoe import TicTacToe
import defaultdict

class TicTacToeManager:

	def __init__(self, msg_writer):
		self.games = defaultdict(lambda: TicTacToe(3,3))
		self.msg_writer = msg_writer

	def get_message(self, channel, message):
		command = message.split()
		if len(command) > 3:
			if command[1].upper() == "START":
				self.start(channel, command[2], command[3])

		if len(command) > 1:
			process_command(channel, command[1])

	def start(self, channel, size, length):
		games[channel] = TicTacToe(size, length)
		self.msg_writer.send_message(channel,tic.__str__())

	def process_command(self, channel, command):
		result = games[channel].process_command(command)
		self.msg_writer.send_message(channel,result)
		if result == True:
			del games[channel]