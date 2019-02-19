import telebot, SQLighter, config, random
from config import database_name
from SQLighter import SQLighter
from telebot import types

def clear_board(chat_id):
    base = SQLighter(database_name)
    base.update_count(chat_id, 0)
    base.update_board(chat_id, '         ')
    base.close()

def update_board(chat_id, i, j, bot):
    base = SQLighter(database_name)
    player = base.select_single(chat_id)
    if player[3][3 * i + j] != ' ':
        return False
    if player[2] == 9:
        return False
    base.update_count(chat_id, player[2] + 1)
    board = player[3][0 : 3 * i + j] + ('X' if (player[1] == 1 and bot) or (player[1] == 0 and not bot) else 'O') + player[3][3 * i + j + 1 : 9]
    base.update_board(chat_id, board)
    base.close()
    return True

def transform_board(board):
    return [[board[0], board[1], board[2]],
            [board[3], board[4], board[5]],
            [board[6], board[7], board[8]]]

def create_markup(chat_id):
    base = SQLighter(database_name)
    player = base.select_single(chat_id)
    board = transform_board(player[3])
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 3        
    for i in range(0, 3):
        keyboard.add(types.InlineKeyboardButton(text=board[i][0], callback_data=str(i) + '0'),
                     types.InlineKeyboardButton(text=board[i][1], callback_data=str(i) + '1'),
                     types.InlineKeyboardButton(text=board[i][2], callback_data=str(i) + '2'))
    base.close()
    return keyboard

def bot_move(chat_id):
    random.seed()
    base = SQLighter(database_name)
    player = base.select_single(chat_id)
    while True:
        i = random.randint(0, 2)
        j = random.randint(0, 2)
        if update_board(chat_id, i, j, False):  
            base.close()
            return True
            
def check_win(chat_id):
    base = SQLighter(database_name)
    player = base.select_single(chat_id)
    base.close()
    if ((player[3][0] != ' ' and player[3][0] == player[3][1] and player[3][1] == player[3][2]) or
        (player[3][3] != ' ' and player[3][3] == player[3][4] and player[3][4] == player[3][5]) or
        (player[3][6] != ' ' and player[3][6] == player[3][7] and player[3][7] == player[3][8]) or
        (player[3][0] != ' ' and player[3][0] == player[3][3] and player[3][3] == player[3][6]) or
        (player[3][1] != ' ' and player[3][1] == player[3][4] and player[3][4] == player[3][7]) or
        (player[3][2] != ' ' and player[3][2] == player[3][5] and player[3][5] == player[3][8]) or
        (player[3][0] != ' ' and player[3][0] == player[3][4] and player[3][4] == player[3][8]) or
        (player[3][2] != ' ' and player[3][2] == player[3][4] and player[3][4] == player[3][6])):
        return True
    return False
