"""
Бот для беседы
"""

import random
import re
import time
from bot_config import *
from vk_api import *
from vk_api.longpoll import *

class Vasilisa(object):
    """Не забудь добавлять докстринг!"""
    # Версия
    VERSION = 1.2

    def __init__(self, token: str, channel: int):
        """ Конструктор """
        self.token = token
        self.channel = channel
        self.session = None
        self.longpoll = None
        self.message = None

        self.IsAliasBegun = False
        self.IsSelectionActive = False
        self.IsAliasActive = False
        self.WordGuess = False
        self.hidden_word, self.hidden_word_key = None, None
        self.turn = 0
        self.queue, self.ind = [], 0
        
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
                        self.message = event.message.lower()
                        if self.IsAliasActive:
                            self.simple_alias(event)
                        else:
                            self.check(event)
            except Exception as e:
                print("Network error:")
                print(e)
                time.sleep(3)
                pass
        
    def send(self, text: str, chat_id: str, reply: int, photo=False):
        """ Отправка сообщения """
        tmp_params = {
            "peer_id": chat_id,
            "message": text,
            "random_id": 0
        }
        # Если надо ответить
        if reply:
            tmp_params["reply_to"] = reply
        # Если надо добавить фото
        if photo:
            tmp_params["attachment"] = f"photo637178190_{random.randint(457239054, 457239199)}"
        # Отправим
        return self.session.method("messages.send", tmp_params)

    def answer_id(self, roster: list, event: {}):
        """ Проверка на наличие индивидуальных ответов """
        return roster[id_list.index(event.user_id) if event.user_id in id_list else 0]

    def check(self, event: {}):
        """ Обработка запроса """
        if not event.from_chat:
            return False
        if event.peer_id != self.channel:
            return False
        
        # Логика общения
        if event.to_me:

            # Функции бота
            if re.search(r"/п[oо]м[oо]щь", self.message):
                text = self.answer_id(assist, event)
                self.send(text, self.channel, event.message_id)
                time.sleep(1)

            # Возвышение Шоты
            elif re.search(r"/ти[pр][aа]н[yу][cс]", self.message):
                text = self.answer_id(tiranus, event)
                self.send(text, self.channel, event.message_id)
                time.sleep(1)

            # Авторы кода
            elif re.search(r"/[cс][oо]зд[aа]т[eе]ли", self.message):
                text = self.answer_id(authors, event)
                self.send(text, self.channel, event.message_id)
                time.sleep(1)

            # Бросок кубика(ов)
            elif re.search(r"/(\d+)d(\d+)", self.message):
                # Исправить для r"/\d*d\d+" обязательно!!!
                match = re.findall(r'\d+', self.message)
                text = '('
                summ = 0
                for i in range(int(match[1])):
                    a = str(random.randint(1, int(match[0])))
                    text += f'{a} + '
                    summ += int(a)
                text = text[:-3] + f') = {summ}'
                self.send(text, self.channel, event.message_id)
                time.sleep(1)

            # Бросок монеты
            elif re.search(r"/м[oо]н[eе]т[aа]", self.message): 
                text = "Орёл!" if random.randint(0, 1) == 0 else 'Решка!'
                self.send(text, self.channel, event.message_id)
                time.sleep(1)

            # Фото природы
            elif re.search(r"/ф[oо]т[oо]", self.message):
                text = self.answer_id(photo, event)
                self.send(text, self.channel, event.message_id, True)
                time.sleep(1)

            # Анекдоты
            elif re.search(r"/[aа]н[eе]кд[oо]т", self.message):
                text = jokes[random.randint(0, len(jokes) - 1)]
                self.send(text, self.channel, event.message_id)
                time.sleep(1)
            # Приветствие
            elif re.search(r"/п[pр]ив[eе]т", self.message) or re.search(r"/[xх][aа]й", self.message) or re.search(r"/[oо][xх][aа]ё", self.message) or re.search(r"/зд[pр][aа]в[cс]тв[yу]й", self.message):
                text = self.answer_id(greeting, event)
                self.send(text, self.channel, event.message_id)
                time.sleep(1)

            # Прощание
            elif re.search(r"/п[oо]к[aа]", self.message) or re.search(r"/быв[aа]й", self.message):              
                text = self.answer_id(farewell, event)
                self.send(text, self.channel, event.message_id)
                time.sleep(1)

            # Id 
            elif "/id" in self.message:
                text = f"Твой id — {event.user_id}"
                self.send(text, self.channel, event.message_id)
                time.sleep(1)

            # Алиас
            elif re.search(r"/иг[pр][aа]", self.message):               
                if re.search(r"п[pр][aа]вил[aа]", self.message):
                    text = rules 
                    self.send(text, self.channel, event.message_id)
                else:
                    text = 'Ну что ж, давайте сыграем.'
                    self.send(text, self.channel, event.message_id)
                    self.IsAliasActive = True
                    self.IsSelectionActive = True
        
        # Иначе ничего
        return False

    def simple_alias(self, event: {}):
        # Вывод правил игры
        if  re.search(r"/иг[pр][aа] п[pр][aа]вил[aа]", self.message):
            text = rules 
            self.send(text, self.channel, event.message_id)
            time.sleep(1)
        if not event.from_chat:
            return False
        if event.peer_id != self.channel:
            return False
        if event.to_me: 
            if "/я" in self.message and self.IsSelectionActive:
                self.queue.append(event.user_id)
                self.send('+', self.channel, event.message_id)
                time.sleep(1)

            elif "/[cс]т[aа][pр]т иг[pр][aа]" in self.message:
                self.IsSelectionActive = False
                text = 'Приём участников в команду закончился =) Начинаем играть!'
                self.send(text, self.channel, event.message_id)
                self.IsAliasBegun = True
                time.sleep(1)
            
            elif self.WordGuess and self.hidden_word_key in self.message:
                if event.user_id == self.queue[self.ind]:
                    text = 'Однокоренные слова нельзя называть!'
                    self.send(text, self.channel, event.message_id)
                    time.sleep(1)
                    self.ind += 1
                else: 
                    if self.hidden_word in self.message:
                        text = 'Молодец! =)'
                        self.send(text, self.channel, event.message_id)
                        time.sleep(1)
                        self.ind += 1
                self.WordGuess = False
            elif not self.IsAliasBegun and re.search(r"/д[aа]", self.message):
                text = 'Отлично, продолжаем!'
                self.send(text, self.channel, event.message_id)
                time.sleep(1)
                self.ind = 0
                self.IsAliasBegun = True
            elif not self.IsAliasBegun and re.search(r"/н[eе]т", self.message):
                text = 'Ладно, сыграем позже...'
                self.send(text, self.channel, event.message_id)
                time.sleep(1)
                self.IsAliasActive = False

        if self.IsAliasBegun:
            if self.ind != len(self.queue) and not self.WordGuess:
                random_key = random.choice(list(dictionary.keys()))
                text = dictionary[random_key]
                self.hidden_word, self.hidden_word_key = text, random_key
                self.send(text, self.queue[self.ind], False)
                time.sleep(1)
                
                self.WordGuess = True

            elif self.ind == len(self.queue) and not self.WordGuess:
                text = 'Круг прошёл. Будем играть дальше?'
                self.send(text, self.channel, False)
                time.sleep(1)
                self.IsAliasBegun = False
                 
        
        return False

        
        
Vasilisa("bbb858ab6e8291e861b37648311578873041b069285db6e4a94e6a9082cf306e00e66594eca81fbc21df8", 2000000004).run()