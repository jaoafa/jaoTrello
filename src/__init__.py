import datetime
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import requests


def init_logger(child_name: str = None) -> logging.Logger:
    _logger = logging.getLogger("sasuke-dinner")
    if child_name is not None:
        _logger = _logger.getChild(child_name)
    dt = datetime.datetime.now().date()
    date_time = dt.strftime("%Y-%m-%d")

    if not os.path.exists("logs/"):
        os.mkdir("logs/")

    rotatedHandler = TimedRotatingFileHandler(
        filename="logs/%s.log" % date_time,
        encoding="UTF-8",
        when="MIDNIGHT",
        backupCount=30
    )
    rotatedHandler.setLevel(logging.INFO)
    rotatedHandler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s'))
    _logger.addHandler(rotatedHandler)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s'))
    _logger.addHandler(streamHandler)

    return _logger


logger = init_logger()


def send_discord_message(token: str, channelId: str, message: str = "", embed: dict = None):
    logger.debug("sendDiscordMessage: {message}".format(message=message))
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bot {token}".format(token=token),
        "User-Agent": "Bot"
    }
    params = {
        "content": message,
        "embed": embed
    }
    response = requests.post(
        "https://discord.com/api/channels/{channelId}/messages".format(channelId=channelId), headers=headers,
        json=params)
    logger.debug("response: {code}".format(code=response.status_code))
    logger.debug("response: {message}".format(message=response.text))


def get_uuid_from_mcid(mcid: str):
    response = requests.get("https://api.jaoafa.com/v1/users/" + mcid)
    if response.status_code != 200:
        return None

    result = response.json()
    if result["status"]:
        return result["data"]["uuid"]

    return None


def get_place_break_count(uuid: str):
    response = requests.get("https://api.jaoafa.com/v1/world/coreprotect/" + uuid + "?info=true")
    if response.status_code != 200:
        return None

    result = response.json()
    if result["status"]:
        return result["data"]["place"], result["data"]["break"]

    return None
