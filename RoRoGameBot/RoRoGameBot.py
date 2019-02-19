# -*- coding: utf-8 -*-
import config, telebot, utils
from SQLighter import SQLighter
from telebot import types

prev_msg = ''

bot = telebot.TeleBot(config.token)

def send_message(chat_id, text, end):
    global prev_msg
    if prev_msg != '':
        bot.delete_message(chat_id, prev_msg)
    if end:
        base = SQLighter(config.database_name)
        base.update_begin(chat_id, 0)
        base.close()
    prev_msg = bot.send_message(chat_id, text, reply_markup=utils.create_markup(chat_id)).message_id

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    text = u"Привет! Я учебный игровой бот. Давай сыграем в крестики-нолики?\nДля начала игры введи /play.\nДля просмотра команд введи /help."
    base = SQLighter(config.database_name)
    if not base.check_player(chat_id):
        base.insert_player(chat_id)
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id    
    text = u"Спсиок игровых команд:\n\n/start - запустить бота.\n/help - получить список команд.\n/play - начать игру в крестики-нолики."
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['play'])
def play(message):
    chat_id = message.chat.id
    base = SQLighter(config.database_name)
    base.update_begin(chat_id, 1)
    base.close()
    utils.clear_board(chat_id)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.row_width = 2
    keyboard.add('Крестик', 'Нолик')
    bot.send_message(chat_id, 'Выбирай: крестик (X) или нолик (O)?', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def text_query(message):
    global prev_msg
    chat_id = message.chat.id
    base = SQLighter(config.database_name)
    if message.text == 'Крестик' or message.text == 'Нолик':
        base.update_badge(chat_id, 1 if message.text == 'Крестик' else 0)
        utils.clear_board(chat_id)
        prev_msg = bot.send_message(chat_id, 'Твой ход!', reply_markup=utils.create_markup(chat_id)).message_id
        base.close()

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    base = SQLighter(config.database_name)
    player = base.select_single(chat_id)
    base.close()
    if player[4] == 1:
        global prev_msg
        i = int(call.data[0])
        j = int(call.data[1])
        if not utils.update_board(chat_id, i, j, True):
            bot.answer_callback_query(call.id, 'Выберите пустую ячейку!')
        else:
            if utils.check_win(chat_id):
                send_message(chat_id, 'Ты победил(а)!', True)
                return
            elif player[2] == 8:
                send_message(chat_id, 'Победила дружба!', True)
                return
            utils.bot_move(chat_id)
            if utils.check_win(chat_id):
                send_message(chat_id, 'Ты проиграл!', True)
                return
            elif player[2] == 7:
                send_message(chat_id, 'Победила дружба!', True)
                return
            send_message(chat_id, 'Твой ход!', False)
    else:
        bot.answer_callback_query(call.id, 'Ты не в игре! Для начала введи /play.')

if __name__ == '__main__':
    bot.polling(none_stop = True)
