import sqlite3

class DatabaseManager:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                value REAL,
                quantity INTEGER
            )
        ''')
        self.connection.commit()

    def add_item(self, item):
        name, value, quantity = item
        self.cursor.execute('''
            INSERT INTO items (name, value, quantity)
            VALUES (?, ?, ?)
        ''', (name, value, quantity))
        self.connection.commit()

    def get_items(self):
        self.cursor.execute("SELECT * FROM items")
        rows = self.cursor.fetchall()
        return rows
    
    def delete_item(self, item):
        name, value, quantity = item
        self.cursor.execute('''
            DELETE FROM items
            WHERE name=? AND value=? AND quantity=?
        ''', (name, value, quantity))
        self.connection.commit()

    def fetch_items(self):
        self.cursor.execute('SELECT name, value, quantity FROM items')
        rows = self.cursor.fetchall()
        items = [(name, value, quantity) for name, value, quantity in rows]
        return items
