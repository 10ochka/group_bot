"""
Бафер для торгового чата
"""

import re
import time
from datetime import timedelta

from vk_api import *
from vk_api.longpoll import *


class Baffer(object):

    # Версия
    VERSION = 2.1

    def __init__(self, token: str, channel: int):
        """ Конструктор """
        self.token = token
        self.channel = channel
        self.session = None
        self.longpoll = None
        self.reg_query = self.compile(r"^1")

    def run(self):
        """ Жизненный цикл """
        print("Initialization...")
        self.session = VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.session)
        print("-> Loaded v%s" % self.VERSION)
        # Пока не выключится
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        self.check(event)
            except Exception as e:
                print("Network error:")
                print(e)
                time.sleep(3)
                pass

    def compile(self, pattern: str):
        """ Сборка регулярки """
        return re.compile(pattern, re.IGNORECASE | re.UNICODE | re.DOTALL | re.MULTILINE)

    def send(self, text: str, reply: int):
        """ Отправка сообщения """
        tmp_params = {
            "peer_id": self.channel,
            "message": text,
            "random_id": 0
        }
        # Если надо ответить
        if reply:
            tmp_params["reply_to"] = reply
        # Отправим
        return self.session.method("messages.send", tmp_params)

    def check(self, event: {}):
        """ Обработка запроса """
        if not event.from_chat:
            return False
        if event.peer_id != self.channel:
            return False
        # Пробьем регулярку
        tmp_match = self.reg_query.search(event.message)
        if tmp_match:
            return self.useBaf(event, tmp_match)
        # Иначе нчиего
        return False

    def useBaf(self, event: {}, match: {}):
        """ Отправим """
        
        self.send("Благословение %s" % match[1], event.message_id)
        time.sleep(3)


Baffer("bbb858ab6e8291e861b37648311578873041b069285db6e4a94e6a9082cf306e00e66594eca81fbc21df8", 2000000004).run()