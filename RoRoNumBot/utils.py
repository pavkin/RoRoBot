# -*- coding: utf-8 -*-

import time, random, config
from SQLighter import SQLighter
from telebot import types

def get_max_score(chat_id):
    base = SQLighter(config.database_name)
    player = base.select_player(chat_id)
    base.close()
    return player[1]

def get_complexity_markup():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 3
    keyboard.add(types.InlineKeyboardButton(text='Легкий', callback_data='easy'),
                 types.InlineKeyboardButton(text='Средний', callback_data='medium'),
                 types.InlineKeyboardButton(text='Сложный', callback_data='hard'))
    return keyboard

def start_game(chat_id, complexity):
    base = SQLighter(config.database_name)
    base.update_cell(config.database_table, config.database_table_columns[2], chat_id, 1)
    base.update_cell(config.database_table, config.database_table_columns[3], chat_id, time.time())
    base.update_cell(config.database_table, config.database_table_columns[5], chat_id, 0)
    base.update_cell(config.database_table, config.database_table_columns[6], chat_id, complexity)
    base.update_cell(config.database_table, config.database_table_columns[7], chat_id, config.settings[complexity][0])
    base.update_cell(config.database_table, config.database_table_columns[8], chat_id, config.settings[complexity][1])
    base.close()

def get_numbers(chat_id):
    base = SQLighter(config.database_name)
    player = base.select_player(chat_id)
    x = random.randint(player[7], player[8])
    y = random.randint(player[7], player[8])
    result = str(x) + ' + ' + str(y) + '?'
    base.update_cell(config.database_table, config.database_table_columns[4], chat_id, x + y)
    base.close()
    return result

def update_time(chat_id):
    base = SQLighter(config.database_name)
    base.update_cell(config.database_table, config.database_table_columns[3], chat_id, time.time())
    base.close()

def check_right_answer(chat_id, query):
    base = SQLighter(config.database_name)
    player = base.select_player(chat_id)
    result = 0
    if player[2] == 0:
        result = 4
    elif not query.isnumeric():
        result = 3
    elif time.time() - player[3] > config.settings[player[6]][2]:
        result = 2
    elif int(query) != player[4]:
        result = 1
    base.close()
    return result

def update_player_settings(chat_id):
    base = SQLighter(config.database_name)
    player = base.select_player(chat_id)
    base.update_cell(config.database_table, config.database_table_columns[5], chat_id, player[5] + 1)
    base.update_cell(config.database_table, config.database_table_columns[7], chat_id, player[7] + config.settings[player[6]][3] / 5)
    base.update_cell(config.database_table, config.database_table_columns[8], chat_id, player[8] + config.settings[player[6]][3])
    base.close()

def finish_game(chat_id):
    base = SQLighter(config.database_name)
    player = base.select_player(chat_id)
    base.update_cell(config.database_table, config.database_table_columns[2], chat_id, 0)
    base.update_cell(config.database_table, config.database_table_columns[1], chat_id, max(player[1], player[5]))
    base.close()
