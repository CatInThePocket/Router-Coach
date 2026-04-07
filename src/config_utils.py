import yaml
from pathlib import Path

def load_config():
    # Since this sits in src/, go up one level to find config.yaml in the root
    root_dir = Path(__file__).parent.parent
    config_path = root_dir / "config.yaml"
    with open(config_path, f"r", encoding="utf-8") as f:
        return yaml.safe_load(f)