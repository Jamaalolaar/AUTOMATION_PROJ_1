import json
class ConfigManager:
    def __init__(self, config_file = "config_file.json"):
        self.config_file = config_file
        self.load_config()
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.config_data = json.load(f)
        except FileNotFoundError:
            print("Config file not found. Setting default config...")
            self.config_data = {}
        except json.JSONDecodeError:
            print("Error: Config file is not a valid JSON.")
            self.config_data = {
            '.txt': 'Text Files',
            '.jpeg': 'Images',
            '.jpg': 'Images',
            '.png': 'Images',
            }

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data,f, indent=2)

    def get_key(self, key, default=None):
        return self.config_data.get(key, default)
    
    def update_config(self, key, value):
        self.config_data[key] = value
        self.save_config()