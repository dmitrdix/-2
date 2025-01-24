import sqlite3



connection = sqlite3.connect("test.db")
cursor = connection.cursor()





def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    ''')
    for i in range(1, 5):
        cursor.execute('INSERT INTO Products(id,title,description,price) VALUES(?,?,?,?)',
                       (f'{i}', f'Продукт {i}', f'Описание {i}', f'{100 * i}'))




def get_all_products():
    cursor.execute("SELECT title, description, price FROM Products")
    products = cursor.fetchall()
    return products

connection.commit()
connection.close()