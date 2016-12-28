#The persistance manager retrieves data from dropbox, and stores a copy in memory. The local copy can be interacted with, and updates will be sent to storage in regular intervals
# do not interact with _data directly! it is a shared resource, and should be inrfaced with using get_data() and update_data()

import logging
import dropbox
from threading import Timer, Lock
from io import StringIO

import config_manager

BACKUP_INTERVAL = 10 * 60 # backup every 10 mins
DATA_LOAD_INTERVAL = 10

class PersistanceManager(object):
	def __init__(self,file_name,seed_file=None):
		self.file_name = file_name
		self.dropbox_client = None
		self._data = None
		self.has_changed = False
		self._start_load_data_worker()
		self.data_lock = Lock()
		self.seed_file = seed_file


	#we need to use getters because of shared resources
	#note that this can be blocking
	def get_data(self):
		if self._data is not None:
			self.data_lock.acquire()
			return_data = self._data
			self.data_lock.release()

			return return_data
		else:
			return None

	def append_to_data(self, s):
		if self._data is not None:
			self.data_lock.acquire()
			self._data += s
			self.data_lock.release()
			self.has_changed = True



	def _start_load_data_worker(self):
		Timer(DATA_LOAD_INTERVAL,self._load_data).start() 

	def _load_data(self):
		logging.info("Loading data")
		if config_manager.config_loaded and config_manager.config["dropbox_access_token"]:
			self.dropbox_client = dropbox.client.DropboxClient(config_manager.config["dropbox_access_token"])
			self.data_lock.acquire()
			try:
				try:
					f,metadata = self.dropbox_client.get_file_and_metadata(self.file_name)
					self._data = f.read();
				except:
					if self.seed_file:
						self._data = self._inject_seed_file()
					else:
						new_file = open("./temp_file", 'w+')
						response = self.dropbox_client.put_file(self.file_name, new_file)
						self._data = ""
				
			finally:
				self.data_lock.release()
				if self._data is None:
					logging.info("Stuff not loaded")
					self._start_load_data_worker()
				else:
					logging.info("stuff loaded")
					logging.info(self._data)
					self._sched_backup()
		else:
			self._start_load_data_worker()

	def _sched_backup(self):
		Timer(BACKUP_INTERVAL,self._run_backup).start() 

	def _run_backup(self):
		logging.info("Starting backup")
		logging.info(self.dropbox_client)
		logging.info(self.has_changed)
		if self.dropbox_client and self.has_changed: 
			self.data_lock.acquire()
			stringFile = StringIO(unicode("".join(i for i in self._data if ord(i)<128), "utf-8"))
			self.dropbox_client.put_file(self.file_name, stringFile, True)
			self.has_changed = False
			self.data_lock.release()
		logging.info("done backup")

		self._sched_backup()

	def _inject_seed_file(self):
		seed = open(self.seed_file, 'r')
		response = self.dropbox_client.put_file(self.file_name, seed)

		new_data = open(self.seed_file, 'r').read()
		seed.close()

		return new_data


