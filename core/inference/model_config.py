import yaml
import os

def load_model_config():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/settings.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('models', {})
    except Exception:
        return {}
