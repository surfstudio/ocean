from urllib.request import urlopen as get


def send_alarm(name, message, config):
    get('https://alarmerbot.ru/?key={0}&message={1}'.format(config[name], message))
