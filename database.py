import mysql.connector


class Database:
    def __init__(self):
        try:
            self.database = mysql.connector.connect(
                host="localhost",
                user="hugodemenez",
                password="password",
                database="stein",
                auth_plugin='mysql_native_password',
            )
            self.cursor = self.database.cursor(buffered=True, dictionary=True)
        except Exception as e:
            raise Exception("Database connection failed")

    def database_request(self, sql, params=None, commit=False, fetchone=False):
        self.cursor.execute(sql, params)
        if commit:
            self.database.commit()
            self.close_connection()
        else:
            results = self.cursor.fetchone() if fetchone else self.cursor.fetchall()
            self.close_connection()
            return results

    def close_connection(self):
        self.cursor.close()
        self.database.close()


    def launch_program(self):
        request = self.database_request("SELECT status FROM program")
        print(request)