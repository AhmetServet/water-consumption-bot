import sqlite3 as sql

class DB:
    def __init__(self, db_file):
        self.conn = sql.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.conn
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, signup_date TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS water_consumption (consumption_id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, amountML INTEGER, FOREIGN KEY(user_id)           REFERENCES users(user_id))')
        self.conn.commit()

    def add_user(self, user_id, username, signup_date):
        self.cursor.execute('INSERT INTO users (user_id, username, signup_date) VALUES (?, ?, ?)', (user_id, username, signup_date))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username=?', (username,))
        self.conn.commit()

    def update_user(self, user_id, username):
        self.cursor.execute('UPDATE users SET username=? WHERE user_id=?', (username, user_id))
        self.conn.commit()

    def add_water_consumption(self, user_id, date, amountML):
        self.cursor.execute('INSERT INTO water_consumption (user_id, date, amountML) VALUES (?, ?, ?)', (user_id, date, amountML))
        self.conn.commit()

    def get_water_consumption(self, user_id, date):
        self.cursor.execute('SELECT * FROM water_consumption WHERE user_id=? AND date=?', (user_id, date))
        return self.cursor.fetchone()

    def get_water_consumption_for_date(self, user_id, start_of_day, end_of_day):
        self.cursor.execute('SELECT * FROM water_consumption WHERE user_id=? AND date BETWEEN ? AND ?', (user_id, start_of_day, end_of_day))
        return self.cursor.fetchall()

    def get_all_water_consumption(self, user_id):
        self.cursor.execute('SELECT * FROM water_consumption WHERE user_id=?', (user_id,))
        return self.cursor.fetchall()

    def update_water_consumption(self, consumption_id, amountML):
        self.cursor.execute('UPDATE water_consumption SET amountML=? WHERE consumption_id=?', (amountML, consumption_id))
        self.conn.commit()

    def delete_water_consumption(self, consumption_id):
        self.cursor.execute('DELETE FROM water_consumption WHERE consumption_id=?', (consumption_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = DB('water-consumptions.db')
    print("",
    db.get_all_users(),
    db.get_all_water_consumption(764516007))
    db.close()
