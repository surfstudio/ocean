from urllib.request import urlopen as get
from urllib.parse import quote


def notify(token, message):
    get("https://alarmerbot.ru/?key={0}&message={1}".format(token, quote(message)))
