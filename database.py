import mysql.connector


class Database:
    def __init__(self):
        self.database = mysql.connector.connect(
            host="localhost",
            user="hugodemenez",
            password="password",
            database="trading",
            auth_plugin='mysql_native_password',
        )
        self.cursor = self.database.cursor(buffered=True, dictionary=True)

    def database_request(self, sql, params=None, commit=False, fetchone=False):
        self.cursor.execute(sql, params)
        if commit:
            self.database.commit()
            self.close_connection()
        else:
            if fetchone:
                results = self.cursor.fetchone()
            else:
                results = self.cursor.fetchall()
            self.close_connection()
            return results

    def close_connection(self):
        self.cursor.close()
        self.database.close()
