from persistance_manager import PersistanceManager 
import config_manager

config_manager.start_config_loader()
p = PersistanceManager("/louds.txt", seed_file="../resources/seed_louds.txt")
