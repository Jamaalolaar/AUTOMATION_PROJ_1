import json
class ConfigManager:
    def __init__(self, config_file = "config_file.json"):
        self.config_file = config_file

        self.load_config()
        self.default_config = {
            "base_path": "C:\\Users\\LENOVO\\Desktop\\AUTOMATION_PROJ_1\\CHAOS",
            "log_files": {
                "Info_log": "Info Logs.log",
                "Error_log": "Error logs.log"
            },
            "extensions": {
                ".txt": "Text Files",
                "jpeg": "Images",
                ".jpg": "Images",
                ".png": "Images",
                ".doc": "Word Documents"}
                }
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.config_data = json.load(f)
        except FileNotFoundError:
            print("Config file not found. Setting default config...")
            self.config_data = self.default_config
        except json.JSONDecodeError:
            print("Error: Config file is not a valid JSON.")
            self.config_data = self.default_config
            
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data,f, indent=2)

    def get(self, key, default=None):
        return self.config_data.get(key, default)
    
    def update_config(self, key, value):
        self.config_data[key] = value
        self.save_config()