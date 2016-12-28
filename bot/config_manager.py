# it is expected that the config is a one line json file

import logging
import os.path
import json
from threading import Timer

CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_PATH = os.path.join("resources",CONFIG_FILE_NAME)
CHECK_INTERVAL = 5


config_loaded = False
config = None


def _check_for_config():
	if not config_loaded and os.path.isfile(CONFIG_FILE_PATH):
		_load_config()
	else:
		Timer(CHECK_INTERVAL,_check_for_config).start()

def _load_config():
	global config, config_loaded

	with open(CONFIG_FILE_PATH) as config_file:
		config = json.loads(config_file.readline());
		config_loaded = True
		print "Loaded config"
		print str(config)


def start_config_loader():
	logging.info("starting cinfig loader")
	Timer(CHECK_INTERVAL,_check_for_config).start()