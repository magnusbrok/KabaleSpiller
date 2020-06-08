import json
from json import JSONEncoder


# https://pynative.com/make-python-class-json-serializable/


class CardDTO:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


class CardEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
