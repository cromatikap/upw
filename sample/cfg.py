import os, yaml

# Get the directory where this module is located
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(_MODULE_DIR, '..', 'config.yml')

# Load configuration once at module import
try:
    with open(_CONFIG_PATH, 'r') as file:
        cfg = yaml.safe_load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"Configuration file not found: {_CONFIG_PATH}")
except yaml.YAMLError as e:
    raise ValueError(f"Error parsing configuration file: {e}") from e

def get(entry):
    """Get a configuration entry."""
    try:
        return cfg[entry]
    except KeyError:
        raise KeyError(f"Configuration entry '{entry}' not found")
