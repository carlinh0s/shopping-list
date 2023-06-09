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

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS item_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                checked INTEGER
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

    def get_item_states(self):
        self.cursor.execute("SELECT * FROM item_states")
        rows = self.cursor.fetchall()
        item_states = {name: bool(checked) for _, name, checked in rows}
        return item_states

    def update_item_state(self, name, checked):
        self.cursor.execute('''
            INSERT OR REPLACE INTO item_states (name, checked)
            VALUES (?, ?)
        ''', (name, int(checked)))
        self.connection.commit()

    def delete_item_state(self, name):
        self.cursor.execute('''
            DELETE FROM item_states
            WHERE name=?
        ''', (name,))
        self.connection.commit()
