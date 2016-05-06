import re

class EquationManager(object):
	
	def solve(self,equation):
		try:
			return "The answer is "+eval(equation)+"!"
		except:
			return "I couldent solve that equation :confounded:"
		
