# -*- coding: utf-8 -*-

import telebot
import config
import utils
from SQLighter import SQLighter

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id

    base = SQLighter(config.database_name)
    if not base.check_player(chat_id):
        base.insert_player(chat_id)
    base.close()
    
    text = 'Привет! Не хочешь сыграть в числа? Для начала напиши /play. Для подробной информации об игре введи /rules. Чтобы посмотреть максимальный счет, напиши /score.'
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['rules'])
def rules(message):
    chat_id = message.chat.id
    text = 'Тебе нужно вывести сумму двух чисел, переданных тебе в сообщении. Сложность возрастает в зависимости от твоего текущего счета (кол-ва верных ответов). На ответ дается некоторое количество секунд, в зависимости от уровня сложности (Легкий - 15, Средний - 10, Сложный - 5), иначе тебе будет засчитано поражение. Удачной игры!'
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['score'])
def score(message):
    chat_id = message.chat.id
    text = 'Твой лучший счет: ' + str(utils.get_max_score(chat_id)) + "."
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['play'])
def play(message):
    chat_id = message.chat.id
    text = 'Выбери уровень сложности:'
    bot.send_message(chat_id, text, reply_markup=utils.get_complexity_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    utils.start_game(chat_id, call.data)
    text = utils.get_numbers(chat_id)
    utils.update_player_settings(chat_id)
    bot.send_message(chat_id, text)
    utils.update_time(chat_id)

@bot.message_handler(content_types=['text'])
def check(message):
    chat_id = message.chat.id
    result = utils.check_right_answer(chat_id, message.text)
    if result == 0:
        text = utils.get_numbers(chat_id)
        utils.update_player_settings(chat_id)
        bot.send_message(chat_id, text)
        utils.update_time(chat_id)
    elif result == 1:
        text = 'Ответ неверный!'
        bot.send_message(chat_id, text)
    elif result == 2:
        text = 'Время закончилось!'
        bot.send_message(chat_id, text)
        utils.finish_game(chat_id)
    elif result == 3:
        text = 'Введи корректное число!'
        bot.send_message(chat_id, text)
    elif result == 4:
        text = 'Ты не в игре! Для начала введи /play.'
        bot.send_message(chat_id, text)

if __name__ == '__main__':
    bot.polling(none_stop = True)
    
