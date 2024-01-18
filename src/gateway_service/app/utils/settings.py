from yaml import safe_load

CONFIG_PATH = "config.yaml"


def get_settings(config_name: str=CONFIG_PATH):
    with open(config_name, 'r') as f:
        data = safe_load(f)

    return data
