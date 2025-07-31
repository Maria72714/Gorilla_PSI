import sqlite3

con = sqlite3.connect('banco.db')
con.execute('PRAGMA foreign_keys = ON')

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

con.execute('''
CREATE TABLE IF NOT EXISTS carrinho (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    prod_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (prod_id) REFERENCES produtos (prod_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)  
''')

con.close()