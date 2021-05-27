# -*- coding: utf-8 -*-
init:
    # Тут находится часть движка использующий Ren'Py script
    screen rpg_interface():

        vbox:
            xalign 1.0
            yalign .5

            first_spacing 30
            spacing 10

            text "Задания:"

            for quest in rpg.quests:

                text str(quest)


init python in rpg:

    """Здесь находится основной движок написанный на Python 2.x"""

    from store import rewards

    quests = []


    def add_quest(quest):
        """Добавляет новый квест"""

        quests.append(quest)

    def finish_quest(quest, won=True):

        """Заканчивает квест, и в случае успешного завершения запускает функцию награды
        если такая есть"""

        if won and callable(quest.reward):

            quest.reward()

        quests.remove(quest)


    def action_handler(action):

        """Обслуживает все действия-ивенты, и определяет есть ли квесты которые ожидают это действие"""

        for quest in quests:

            if action.action_name == quest.action_name:
                quest.handler(action)


    class Quest:

        """Базовый класс квеста"""

        def __init__(self, action_name, reward, text=""):

            self.action_name = action_name
            self.reward = reward

            self.text = text or action_name

        def handler(self, action, *args, **kwargs):

            """Если именнованое событие произошло - сразу завершение квеста с победой"""

            print(action)

            finish_quest(self, True)

        def __str__(self):

            return self.text

    class QuestAction:

        """Класс действий"""

        def __init__(self, action_name, *args, **kwargs):
            self.action_name = action_name

            self.args = args
            self.kwargs = kwargs

    class BeingNyasha(Quest):

        """Тестовый квест проверяющую логику унаследование главного класса квестов
        и упрощение тестов механики получение-завершение квестов"""

        def __init__(self):

            super(BeingNyasha, self).__init__("nya", rewards.Congrats("Ты някнул!"), "Дочитать текст")

init python in rewards:

    """ Модуль с заготовками для функций "наград" """

    class Congrats:
        """По сути аналогична классу Notify"""
        def __init__(self, text):
            self.text = text

        def __call__(self):

            renpy.notify(self.text)
