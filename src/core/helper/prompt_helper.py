from enum import IntEnum, auto
import json
from core.errors.error import unexpectedInputError


class promptType(IntEnum):
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    QUESTION = auto()


class promptHelper:
    def __init__(self, filename: str, /):
        self.filename = filename

    def load_config(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
        self.config = data
        self.log_format = self.config["log_format"]

    def log(self, prompt: str, type: promptType = promptType.INFO, /):
        if type == 1:
            print(self.log_format["info"] + prompt)
        elif type == 2:
            print(self.log_format["warn"] + prompt)
        elif type == 3:
            print(self.log_format["error"] + prompt)
        elif type == 4:
            return input(self.log_format["question"] + prompt + " : ")
        else:
            raise unexpectedInputError(
                "The type parameter is not an integer or a messageType class constant."
            )
