from urllib.request import urlopen as get
from urllib.parse import quote
from .coordinator import ExperimentCoordinator


def notify(usernames, message):
    tokens = []

    if usernames == 'all':
        tokens = ExperimentCoordinator().alarm_config.values()
    else:
        usernames = usernames.split(",")
        for username in usernames:
            tokens.append(ExperimentCoordinator().alarm_config[username])
    for token in tokens:
        get("https://alarmerbot.ru/?key={0}&message={1}".format(token, quote(message)))
