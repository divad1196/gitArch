import os
from pathlib import Path
import json
import yaml

def load_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def json_dump(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

def parent_dir(path):
    return Path(os.path.dirname(Path(path).resolve()))

def load_yaml(file):
    with open(file, "r") as f:
        data = yaml.safe_load(f)
    return data

def dump_yaml(file, data):
    with open(file, "w") as f:
        yaml.dump(data, f, default_flow_style=False)