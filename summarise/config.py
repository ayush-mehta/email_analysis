from json import load

def load_config():
    with open('config.json', 'r') as f:
        return load(f)

config = load_config()