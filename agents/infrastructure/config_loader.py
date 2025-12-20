import os
import yaml

class ConfigLoader:
    """Hierarchical configuration loader"""

    def __init__(self):
        self.config = {}

    def load(self):
        """Load configuration from multiple sources"""
        # 1. Load defaults
        self.config = {
            "LOG_LEVEL": "info",
            "REDIS_URL": "redis://localhost:6379"
        }

        # 2. Load from YAML config file if exists
        try:
            with open("config.yaml", 'r') as f:
                yaml_config = yaml.safe_load(f) or {}
                self.config.update(yaml_config)
        except FileNotFoundError:
            pass

        # 3. Override with environment variables
        for key in self.config.keys():
            env_val = os.getenv(key)
            if env_val is not None:
                self.config[key] = env_val

        return self

    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)