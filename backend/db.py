import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime
import pandas as pd

def md5_hash(string):
    # Create an instance of the MD5 hash object
    md5 = hashlib.md5()

    # Encode the string as bytes and hash it
    md5.update(string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_string = md5.hexdigest()

    return hashed_string

class DB:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.connect()
        print(self.connection.get_server_info())
        self.connection.close()

    def initdb(self) -> bool:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("drop table if exists profile;")
        cursor.execute("""
        create table profile 
            (
            id int AUTO_INCREMENT PRIMARY KEY,
            username varchar(40) NOT NULL,
            password varchar(40) NOT NULL,
            email varchar(255) NOT NULL,
            description TEXT NOT NULL,
            applied_date varchar(10),
            closed_date varchar(10),
            timestamp DATETIME NOT NULL,
            status varchar(10) NOT NULL
            );
            """)
        self.connection.commit()
        return True

    def connect(self):
        self.connection = mysql.connector.connect(host=self.host, database='sgprapp',
                                            user=self.user,
                                            password=self.password)
        
    def add_row(self, username, password, email, status, description, applied_date, closed_date, mode="create") -> str:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"select * from profile where username = \'{username}\'")
        res = cursor.fetchall()
        if len(res) > 0 and mode == "create":
            return "user is already existed"
        
        cursor.execute(f"""
                       INSERT INTO profile (username, password, email, description, applied_date, closed_date, timestamp, status) 
                       VALUES (
                       \'{username}\', \'{password}\', 
                       \'{email}\', \'{description}\',  \'{applied_date}\',  \'{closed_date}\', 
                       \'{datetime.now().strftime('%Y-%m-%d %T')}\', \'{status}\');
                       """)
        self.connection.commit()
        self.connection.close()
        return "ok"
        
    def verify_user(self, username, password) -> list:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"""
                       select username, email, description, applied_date, closed_date, status from profile 
                       where username = \'{username}\' and password = \'{password}\'
                       order by timestamp desc
                       limit 1;
                       """)
        res = cursor.fetchall()
        if len(res) > 0:
            return pd.DataFrame(res, 
                                columns=['username', 'email', 'description', 'applied_date', 'closed_date', 'status']
                                ).to_dict(orient='records')[0]
        return None
        
    def fetch_all(self, nrows = 0):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('select id, username, description, timestamp, status, applied_date, closed_date from profile order by timestamp desc;')
        df = cursor.fetchall()
        self.connection.close()
        df = pd.DataFrame(df, columns=['id','username', 'description', 'datetime','status', 'applied_date', 'closed_date'])
        df['rank'] = df.groupby('username', as_index = False)['datetime'].rank(ascending=False)
        df = df.query("rank == 1")
        if nrows > 0:
            df = df[:nrows]
        return df.to_dict(orient='records')
