from loguru import logger
import json, sys
import argparse
from enum import Enum

class Action(Enum):
    update = "update"
    delete = "delete"

class ParseMode(Enum):
    Null = None
    html = "HTML"
    md = "Markdown"
    md2 = "Markdownv2"

class JSONWithCommentsDecoder(json.JSONDecoder):
    def __init__(self, **kw):
        super().__init__(**kw)

    def decode(self, s: str):
        s = '\n'.join(l if not l.lstrip().startswith('//') else '' for l in s.split('\n'))
        return super().decode(s)

class BotConfig:
    def __init__(self, data: dict):
        if not data:
            logger.warning("Bot settings not configure use default")
            self.token = None
            return
        self.token = data.get("token")
        if not self.token:
            logger.warning("Bot token is empty. Try get from env: BOT_TOKEN")
        else:
            self.token = str(self.token)
class DbConfig:
    def __init__(self, data):
        if not data:
            logger.warning("Database settings not configure use default")
            self.mode = 0
            return
        self.mode = 1 if "dev" not in data["mode"].lower() else 0
        if self.mode: # TODO
            ...

class Config:
    def __init__(self, path: str):
        self.src = self.read_file(path)
        if self.src == {}:
            logger.error(f"file [{path}] not found or empty. Read docs")
        self.admins = self.src.get("admins") or []
        self.bot = BotConfig(self.src.get("bot"))
        self.database = DbConfig(self.src.get("database"))
        self.debug = self.src.get("debug") or True

    @staticmethod
    def read_file(path: str):
        try:
            with open(path, "r") as f:
                return json.loads(f.read(), cls=JSONWithCommentsDecoder)
        except FileNotFoundError:
            return {}
        
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Path to config file", default="config.json")
    return parser.parse_args()

