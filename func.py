from datetime import datetime

def say_hi():
    time_to_start = datetime.now().hour
    if time_to_start>=6 and time_to_start<=11:
        ToD = 'Доброе утро!'
    if time_to_start>=12 and time_to_start<=19:
        ToD = 'Добрый день!'
    if time_to_start >= 20 and time_to_start <= 0:
        ToD = 'Добрый вечер!'
    if time_to_start >= 21 and time_to_start <= 5:
        ToD = 'Доброй ночи!'
    hello_message = '{} Представся пожалуйста!'.format(ToD)
    return hello_message

