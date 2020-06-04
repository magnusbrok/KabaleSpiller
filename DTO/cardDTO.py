import json
from json import JSONEncoder


class CardDTO:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


class CardEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
