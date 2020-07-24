from urllib.request import urlopen
from urllib.parse import quote as urlquote
from json import loads

DEFINE_URL = 'https://api.urbandictionary.com/v0/define?term='
RANDOM = 'https://api.urbandictionary.com/v0/random'


class UrbanDictionary(object):
    def __init__(self, exist: bool, word: str, definition: str, example: str, upvotes: int, downvotes: int):
        self.exist = exist
        self.word = word
        self.definition = definition
        self.example = example
        self.upvotes = upvotes
        self.downvotes = downvotes

    def __str__(self):
        return f"{self.word}, {self.definition[:50]}, ( UP {self.upvotes} DOWN{self.downvotes} )"

    def __contains__(self, param1):
        return param1 in self.__dict__.keys()


def getud(url):
    f = urlopen(url)
    data = loads(f.read().decode('utf-8'))
    f.close()
    return data


def parse_data(json):
    if json is None or any(e in json for e in ('error', 'errors')):
        raise ValueError('Cannot find term on Urban Dictionary')
    if len(json['list']) == 0:
        return [UrbanDictionary(exist=False)]
    return [UrbanDictionary(
        True,
        definition['word'],
        definition['definition'],
        definition['example'],
        int(definition['thumbs_up']),
        int(definition['thumbs_down'])) for definition in json['list']]


def define(word):
    json = getud(f"{DEFINE_URL}{urlquote(word)}")
    return parse_data(json)


def random():
    json = getud(RANDOM)
    return parse_data(json)
