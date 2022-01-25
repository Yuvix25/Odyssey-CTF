import sqlite3

EXAMPLE_PASSWORDS = {
    "yoavsus": "ja8AJl92Kks",
    "yossi": "yossi",
    "banana23": "password1234",
    "level5": "uX0ffyrHStMzUDkEoLu6PcfcDlZCAQc1",
}

class Database:
    def __init__(self):
        self.db = sqlite3.connect('odysseyctf.db', check_same_thread=False)

        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS passwords (username VARCHAR(255), password VARCHAR(255))")

        # clear table:
        self.cursor.execute("DELETE FROM passwords")

        for username, password in EXAMPLE_PASSWORDS.items():
            sql = f"INSERT INTO passwords (username, password) VALUES ('{username}', '{password}')"
            self.cursor.execute(sql)

        self.db.commit()

        print("SQLite ready.")
    
    def execute_read_only(self, query):
        try:
            self.db.commit()
        except Exception as e:
            print("First try:", e)
        
        
        self.cursor.execute(query)
        self.db.rollback()

    
    def validate_login(self, username, password):
        sql = f'SELECT * FROM passwords WHERE username = "{username}" AND password = "{password}"'
        self.execute_read_only(sql)
        result = self.cursor.fetchone() is not None

        if result:
            sql = f'SELECT password FROM passwords WHERE username = "{username}"'
            self.execute_read_only(sql)
            result = self.cursor.fetchone()
            if result:
                return result[0]