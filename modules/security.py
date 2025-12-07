import json
import os
from modules.debug_logger import logger

class Security:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        try:
            if not os.path.exists(self.config_path):
                logger.error(f"Config file not found: {self.config_path}")
                return {}

            with open(self.config_path, 'r') as f:
                config = json.load(f)
                logger.info("Configuration loaded successfully.")
                return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}

    def get(self, key, default=None):
        return self.config.get(key, default)

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
         try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
                logger.info("Configuration saved successfully.")
         except Exception as e:
            logger.error(f"Failed to save config: {e}")

# Global instance
security = Security()
