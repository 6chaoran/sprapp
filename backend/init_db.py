from db import DB
db = DB()
if db.initdb():
    print('database is initiated.')