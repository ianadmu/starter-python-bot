import re

class EquationManager(object):
	
	def solve(self,equation):
		tokens = equation.split()
		if(tokens.length != 3):
			return "Ask me to solve an equation by saying 'zac solve <equation>'"

		try:
			return "The answer is "+eval(tokens[3])+"!"
		except:
			return "I couldent solve that equation :confounded:"
		
