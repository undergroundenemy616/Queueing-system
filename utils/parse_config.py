import configparser


def parse_config(section, key):
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config[section][key]
