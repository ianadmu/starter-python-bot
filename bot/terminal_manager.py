import logging
import subprocess
import time
from threading import Timer

MAX_RUN_TIME = 5

logger = logging.getLogger(__name__)

def run_terminal_command(command):
	logging.info("GOT COMMAND")
	logging.info(command)
	command_array = command.replace("&gt;",">").split()[1:]
	logging.info(command_array)

	control_vars = {
		"command_tokens" : command_array,
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

		if control_vars["process_killed"]:
			return "I took to long to run a command!"
	 	elif error:
	 		logging.info("Error: "+error)
	 		return "Something went wrong while executing that command: "+error
	 	else:
	 		logging.info("output: "+output)
	 		return "> "+output


	def _dead_man_swicth():
		if not control_vars["command_completed"]:
			if control_vars["process"]:
				control_vars["process_killed"] = True
				control_vars["process"].kill()	

	control_vars["dead_man_swicth_timer"] = Timer(MAX_RUN_TIME, _dead_man_swicth)
	return _run_command_wrapper()