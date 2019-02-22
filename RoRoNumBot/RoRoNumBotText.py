import telebot, random, time, config
from telebot import types

bot = telebot.TeleBot(config.token)

temp_time = time.time()
answer = 0
score = 0
left = 0
right = 0 # @RoRoNumBot
add_left = 0
add_right = 0

def show_numbers(chat_id):
    global answer
    global right
    global left
    global add_right
    global add_left
    x = random.randint(left, right)
    y = random.randint(left, right)
    answer = x + y
    left += add_left
    right += add_right
    text = str(x) + ' + ' + str(y) + '?'
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['start', 'help'])
def get_help(message):
    chat_id = message.chat.id
    text = 'Привет! Вот список команд:\n\n/start - запустить бота.\n/rules - правила игры.\n/play - начать игру.'
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['rules'])
def get_rules(message):
    chat_id = message.chat.id
    text = 'Тебе нужно вывести сумму двух чисел, переданных тебе в сообщении. Сложность возрастает в зависимости от твоего текущего счета (кол-ва верных ответов). На ответ дается 10 секунд, иначе тебе будет засчитано поражение. Удачной игры!'
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['play'])
def play(message):
    chat_id = message.chat.id
    global score
    score = 0
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 3
    keyboard.add(types.InlineKeyboardButton(text='Простой', callback_data='easy'),
                types.InlineKeyboardButton(text='Средний', callback_data='medium'),
                types.InlineKeyboardButton(text='Сложный', callback_data='hard'))
    bot.send_message(chat_id, 'Выбери уровень сложности:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    global temp_time
    global right
    global left
    global add_right
    global add_left
    if (call.data == 'easy'):
        left = 0
        right = 10
        add_left = 3
        add_right = 5
    elif (call.data == 'medium'):
        left = 3
        right = 15
        add_left = 5
        add_right = 8
    elif (call.data == 'hard'):
        left = 5
        right = 20
        add_left = 8
        add_right = 13
    show_numbers(chat_id)
    temp_time = time.time()

@bot.message_handler(content_types=['text'])
def check(message):
    chat_id = message.chat.id
    text = message.text
    if (text.isnumeric()):
        ans = int(text)
        global answer
        if (ans == answer):
            global temp_time
            global score
            global right
            global left
            if (time.time() - temp_time < 10.0):
                show_numbers(chat_id)
                temp_time = time.time()
                score += 1
            else:
                config.max_score = max(config.max_score, score)
                text = 'Сочувствую, ты проиграл(а)! Твой счет: ' + str(score * 10) + '.'
                bot.send_message(chat_id, text)
        else:
            bot.send_message(chat_id, "Ответ неверный!")
    else:
        bot.send_message(chat_id, "Введи корректное число!")

if __name__ == '__main__':
    bot.polling(none_stop = True)
