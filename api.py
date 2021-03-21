# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
from func import *
from todoist import *

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

from todoist_module import *

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Катя",
                "Влад",
                "Другое",
            ]
        }

        hello_message = say_hi()

        res['response']['text'] = hello_message
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req ['request'] ['original_utterance'].lower () in [
        'катя',
        'екатерина',
        'катюша',
        'красавица']:
        sessionStorage [user_id] = {}

        sessionStorage [user_id] = {
            'suggests': [
                "Добавить заметку",
                "Назначить событие",
                "Надиктовать идеи и мысли"
            ]
        }

        res ['response'] ['text'] = 'Рада вас видеть! Что вы хотите сделать?'
        res ['response'] ['buttons'] = get_suggests (user_id)
        return

    if req['request']['original_utterance'].lower () in [
        'добавить заметку',
        'создать заметку',
        'сформировать заметку',
        'заметку']:

        api = start_todoist ()

        sessionStorage [user_id] = {}

        lst_projects = pars_responce (api)

        sessionStorage [user_id] = {
            'API': [
                "True"
            ],
            'suggests': lst_projects
        }

        res ['response'] ['text'] = 'А в какой проект вы хотите записать это?'
        res ['response'] ['buttons'] = get_suggests (user_id)
        return


    if req['request']['original_utterance'].lower () in [
        'добавить заметку',
        'создать заметку',
        'сформировать заметку',
        'заметку']:

        start_todoist ()

        sessionStorage [user_id] = {
            'note': [
                "True"
            ]
        }

        res ['response'] ['text'] = 'Отлично, записываю'
        res ['response'] ['buttons'] = get_suggests (user_id)
        return



# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests']
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests
