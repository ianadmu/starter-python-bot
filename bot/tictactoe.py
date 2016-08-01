import random
import re

class Line:
	k = 3
	#k is a konstant weighting factor

	def __init__(self, length):
		self.length = length
		self.current_size = 0
		self.owner = 0

	def get_score(self, player):
		if player == self.owner and self.length == self.current_size + 1:
			return float("inf")

		if player != self.owner:
			return (self.current_size + 3) ** Line.k

		return (self.current_size + 2) ** Line.k

	def play(self, player):
		#returns -1 when the line becomes impossible to win on
		#1 on a victory
		#0 on all other normal events
		if self.owner == 0:
			self.owner = player

		if self.owner != player:
			#this means that victory cannot happen on this line and it should be removed
			self.owner = -1
			self.current_size = 0
		else:
			self.current_size += 1
			if self.current_size == self.length:
				return True
		return False

	def __str__(self):
		return ' >' + str(self.owner) + ' ' + str(self.current_size) + '<'


class BoardSpot:
	tokens = [' ', 'O', 'X']

	def __init__(self):
		self.value = 0
		self.lines = set()

	def play(self, player):
		if self.value == 0:
			self.value = player
			for line in self.lines:
				result = line.play(self.value)
				if result == True:
					return True
		else:
			raise Exception(player + " Tried to override a spot on the board")

		return False

	def update_lines(self):
		self.lines = filter(lambda line: line.owner != -1, self.lines)

	def get_score(self, player):
		score = 0
		for line in self.lines:
			score += line.get_score(player)
		return score

	def get_token(self):
		return BoardSpot.tokens[self.value]

	def get_value(self):
		return self.value

	def change_tokens(self):
		BoardSpot.tokens[1], BoardSpot.tokens[2] = BoardSpot.tokens[2], BoardSpot.tokens[1]

	def __str__(self):
		lines_str = "Lines: "
		for line in self.lines:
			if line.owner != -1:
				lines_str += line.__str__()
		return lines_str + "\n" + self.get_token()

	def add_line(self, line):
		self.lines.add(line)

class TicTacToe:

	def __init__(self, size, line_size):
		if size < 3:
			size = 3
		elif size > 10:
			size = 10

		self.line_size = line_size
		self.winner = False
		self.comp_player = 1
		self.human_player = 2
		self.size = size
		self.turn = random.choice([True, False])
		self.board = [[BoardSpot() for x in range(size)] for y in range(size)]
		self.open_spots = self._get_all_spots()
		self.add_lines_to_board()
		if self.turn:
			self._self_move()

	def process_command(self, message):
		if self._is_over():
			return "Game is over"
		if self.player_move(message):
			#success full move
			if self._is_over():
				print("You win!")
				return True
			else:
				self._self_move()
				if self._is_over():
					print("Zac wins!")
					return True

			return(self.__str__())
		else:
			return self._get_move_error(message)

	def _is_over(self):
		return not self.open_spots or self.winner

	def start_game(self):
		while self.open_spots and not self.winner:
			self.turn = not self.turn
			if self.turn:
				self._self_move()
			else:
				move = raw_input(self)
				self.player_move(move)
		if self.winner:
			if self.turn:
				message = "Zac wins!"
			else:
				message = "You win!"
			print(message)
		print(self)

	def add_lines_to_board(self):
		line_directions = [(0,1),(1,0),(1,1),(1,-1)]
		#right now the lines are the same length as the board
		for x in range(self.size):
			for y in range(self.size):
				for direction in line_directions:
					spots_in_line = self.get_spots_for_line((x,y), direction, self.line_size)
					line = Line(self.line_size)
					for spot_to_add in spots_in_line:
						spot_to_add.add_line(line)


	def get_spots_for_line(self, start, direction, length):
		#if the line would go over the board, an empty list is returned instead
		x = start[0]
		y = start[1]

		spots = []
		if x == 2 and y == 2 and direction == (-1,-1):
			print(x + (direction[0] * length))

		if x + (direction[0] * length) > self.size or x + (direction[0] * length) < -1:
			return spots

		if y + (direction[1] * length) > self.size or y + (direction[1] * length) < -1:
			return spots

		for step in range(length):
			current_x = x + (direction[0] * step)
			current_y = y + (direction[1] * step)
			spots.append(self.board[current_x][current_y])

		return spots

	def _self_move(self):
		comp_move = self._find_best_move()
		self.winner = self._move(self.comp_player, comp_move)
		self._update_lines()

	def _update_lines(self):
		for spot in self.open_spots:
			spot.update_lines()

	def _move_randomly(self):
		return random.choice(self.open_spots)

	def _find_best_move(self):
		moves = sorted(self.open_spots, key=lambda spot: spot.get_score(self.comp_player), reverse=True)
		return moves[0]

	def _get_all_spots(self):
		spots = []
		for row in self.board:
			for spot in row:
				spots.append(spot)
		return spots

	def tokenize(self, spot):
		return spot.get_token()

	def __str__(self):
		blank = '   ' + '|'.join(["   "] * self.size) + '\n'
		middle = " | "
		line = '   ' + ('-' * ((4 * self.size) - 1))
		rows = []
		top_row = '    ' + "   ".join(map(str,range(self.size))) + '\n'
		for row_index in range(self.size):
			result = '\n' + blank + ' '
			result += chr(ord('A') + row_index) + '  ' + middle.join(map(self.tokenize, self.board[row_index]))
			result += ' \n' + blank
			rows.append(result)

		return top_row + line.join(rows)

	def _move(self, player, spot):
		self.open_spots.remove(spot)
		return spot.play(player)

	def _getY(self, move):
		#don't even ask why these seem to be reversed
		numbers = re.sub('[^0-9]','', move)
		if numbers:
			return int(numbers)
		else:
			return None

	def _getX(self, move):
		char = re.sub('[^A-Z]','', move.upper())
		if char:
			return ord(char[0]) - ord('A')
		else:
			return None

	def _get_move_error(self, move):
		x = self._getX(move)
		y = self._getY(move)
		if x == None:
			return "You must have at least one letter"
		elif y == None:
			return "You must have at least one number"
		elif x > self.size:
			return "You must input a valid Row"
		elif y > self.size:
			return "You must input a valid Column"
		elif self.board[x][y] not in self.open_spots:
			return "You must select an empty spot"
		return "Unknown Error"

	def _parse_move(self, move):
		x = self._getX(move)
		y = self._getY(move)
		if (x == None or y == None or x > self.size or x < 0 or y > self.size or y < 0) or self.board[x][y] not in self.open_spots:
			return (None,None)
		return (x,y)

	def player_move(self,move):
		coordinates = self._parse_move(move)
		if None in coordinates:
			return False
		self.winner = self._move(self.human_player, self.board[coordinates[0]][coordinates[1]])
		return True