# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

#Собственные модули
from func import *
from todoist_module import *

# Модули для работы с JSON и логами.
import json
import logging

# Подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

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

if __name__ == "__main__":
    app.run(debug = False)