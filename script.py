import sqlite3

connection = sqlite3.connect('recipe_database.db')
cursor = connection.cursor()


cursor.execute('''
               CREATE TABLE IF NOT EXISTS recipes(
               id INTEGER PRIMARY 
               )
               )