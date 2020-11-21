import yaml

with open('config.yml', 'r') as file:
    cfg = yaml.safe_load(file)

def get(entry):
    return cfg[entry]
