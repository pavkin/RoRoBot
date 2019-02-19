# -*- coding: utf-8 -*-
import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM players').fetchall()

    def select_single(self, chat_id):
        """ Получаем одну строку по игроку chat_id """
        with self.connection:
            return self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id,)).fetchall()[0]
    
    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM players').fetchall()
            return len(result)

    def check_player(self, chat_id):
        """ Проверить, есть ли пользователь chat_id в базе """
        with self.connection:
            players = self.cursor.execute('SELECT * FROM players WHERE chat_id = ?', (chat_id, )).fetchall()
            if len(players) == 0:
                return False
            else:
                return True
            
    def insert_player(self, chat_id):
        """ Добавляем нового пользователя """
        with self.connection:
            self.cursor.execute('INSERT INTO players VALUES(?,?,?,?)', (chat_id, 0, 0, '         '))
            self.connection.commit()

    def update_badge(self, chat_id, badge):
        """ Обновляем badge для пользователя chat_id """
        with self.connection:
            self.cursor.execute("UPDATE players SET badge = " + str(badge) + " WHERE chat_id = '" + str(chat_id) + "'")
            self.connection.commit()
        
    def update_count(self, chat_id, count):
        """ Обновляем badge для пользователя chat_id """
        with self.connection:
            self.cursor.execute("UPDATE players SET count = " + str(count) + " WHERE chat_id = '" + str(chat_id) + "'")
            self.connection.commit()

    def update_board(self, chat_id, board):
        """ Обновляем badge для пользователя chat_id """
        with self.connection:
            self.cursor.execute("UPDATE players SET board = '" + str(board) + "' WHERE chat_id = '" + str(chat_id) + "'")
            self.connection.commit()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
