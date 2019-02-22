# -*- coding: utf-8 -*-

import sqlite3

class SQLighter:

    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def select_player(self, chat_id):
        """ Получаем одну строку по игроку chat_id """
        with self.connection:
            return self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id,)).fetchall()[0]

    def check_player(self, chat_id):
        """ Проверить, есть ли пользователь chat_id в базе """
        with self.connection:
            players = self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()
            if len(players) == 0:
                return False
            return True
            
    def insert_player(self, chat_id):
        """ Добавляем нового пользователя """
        with self.connection:
            self.cursor.execute('INSERT INTO players VALUES(?,?,?,?,?,?,?,?,?)', (chat_id, 0, 0, 0, 0, 0, 'easy', 0, 0))
            self.connection.commit()

    def update_cell(self, table, cell, chat_id, value):
        """ Обновляем поле cell в таблице table значением value для пользователя chat_id """
        with self.connection:
            text = 'UPDATE ' + str(table) + ' SET ' + str(cell) + " = ? WHERE chat_id = '" + str(chat_id) + "'"
            self.cursor.execute(text, (value, ))
            self.connection.commit()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
