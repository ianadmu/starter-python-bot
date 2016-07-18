import re

class EquationManager(object):

	def solve(self,equation):

		tokens = equation.split()
		if(len(tokens)!= 3):
			return "Ask me to solve an equation by saying 'zac solve <equation>'"

		try:
			if "__import__" in tokens[2]:
				return "stop messing around taylor :camel:"
			else:
				return "The answer is "+str(eval(tokens[2]))+"!"
		except:
			return "I coulden't solve that equation :confounded:"
