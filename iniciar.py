import sqlite3

con = sqlite3.connect('banco.db')
con.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL
)
''')

con.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_nome VARCHAR(255) NOT NULL,
    prod_valor FLOAT NOT NULL
)
''')
con.close()