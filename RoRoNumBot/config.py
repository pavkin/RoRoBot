# -*- coding: utf-8 -*-

token = 'YOUR_TOKEN'

database_name = 'nums.db'
database_table = 'players'
database_table_columns = ['chat_id', 'max_score', 'game_start', 'game_time', 'game_right_answer',
                          'game_score', 'game_complexity', 'game_left_seed', 'game_right_seed']

settings = { 'easy': [5, 10, 15, 5],
             'medium': [10, 15, 10, 10],
             'hard': [15, 20, 5, 15] }

left_easy = 5
right_easy = 10
time_seed_easy = 15
random_seed_easy = 5

left_medium = 10
right_medium = 15
time_seed_medium = 10
random_seed_medium = 10

left_hard = 15
right_hard = 20
time_seed_hard = 5
random_seed_hard = 15
