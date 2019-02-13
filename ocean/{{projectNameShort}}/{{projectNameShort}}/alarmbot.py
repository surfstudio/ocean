from urllib.request import urlopen as get


def notify(token, message):
    get('https://alarmerbot.ru/?key={0}&message={1}'.format(token, message))
