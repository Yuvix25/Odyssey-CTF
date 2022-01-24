import mysql.connector

EXAMPLE_PASSWORDS = {
    "yoavsus": "ja8AJl92Kks",
    "yossi": "yossi",
    "banana23": "password1234",
    "level5": "uX0ffyrHStMzUDkEoLu6PcfcDlZCAQc1",
}

class Database:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="db4free.net",
            user="odysseyctf",
            passwd="uvQvD5K6@fHt",
        )

        self.mycursor = self.mydb.cursor(buffered=True)
        self.mycursor.execute("USE odysseyctf")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS passwords (username VARCHAR(255), password VARCHAR(255))")

        # clear table:
        self.mycursor.execute("DELETE FROM passwords")

        for username, password in EXAMPLE_PASSWORDS.items():
            sql = "INSERT INTO passwords (username, password) VALUES (%s, %s)"
            val = (username, password)
            self.mycursor.execute(sql, val)

        self.mydb.commit()

        print("MySQL connection is ready")
    
    def execute_read_only(self, query, params=None):
        try:
            self.mydb.commit()
        except Exception as e:
            print("First try:", e)
        
        try:
            self.mycursor.execute("SET TRANSACTION READ ONLY")
            self.mycursor.execute(query, params)
        except Exception as e:
            print("Second try:", e)
            return "Error"
    
    def validate_login(self, username, password):
        sql = f'SELECT * FROM passwords WHERE username = "{username}" AND password = "{password}"'
        self.execute_read_only(sql)
        result = self.mycursor.fetchone() is not None

        if result:
            sql = f'SELECT password FROM passwords WHERE username = "{username}"'
            self.execute_read_only(sql)
            result = self.mycursor.fetchone()[0]
            return result