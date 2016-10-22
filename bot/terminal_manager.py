import subprocess
import time
from threading import Timer

MAX_RUN_TIME = 5

def run_terminal_command(command):
	control_vars = {
		"command_tokens" : command.split()[1:],
		"command_completed" : False,
		"process" : None,
		"process_killed" : False,
		"dead_man_swicth_timer" : None
	}

	def _run_command_wrapper():
		process = subprocess.Popen(control_vars["command_tokens"], stdout=subprocess.PIPE)
		control_vars["process"] = process
		control_vars["dead_man_swicth_timer"].start()
		output, error = process.communicate()
		control_vars["command_completed"] = True

		if process_killed:
			return "I took to long to run a command!"
	 	elif error:
	 		return "Something went wrong while executing that command: "+error
	 	else:
	 		return output


	def _dead_man_swicth():
		if not control_vars["command_completed"]:
			if control_vars["process"]:
				control_vars["process"].kill()	

	control_vars["dead_man_swicth_timer"] = Timer(MAX_RUN_TIME, terminal_manager._dead_man_swicth).start()
	return terminal_manager._run_command_wrapper()