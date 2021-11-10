from database import Database



print(Database().database_request(sql="""SELECT * FROM telegram""",fetchone=True))