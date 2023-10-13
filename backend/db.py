import mysql.connector
import hashlib
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine


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
        self.port = port = 3306
        self.schema = schema = 'sgprapp'
        self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{schema}', echo = False)
        self.connect()
        print(self.connection.get_server_info())
        self.connection.close()

    def initdb(self, uat = False) -> bool:
        self.connect()
        cursor = self.connection.cursor()
        tablename = 'uat_profile' if uat else 'profile'
        cursor.execute(f"drop table if exists {tablename};")
        cursor.execute(f"""
        create table {tablename} 
            (
            id varchar(50) NOT NULL,
            id_hash TEXT NOT NULL,
            username varchar(40) NOT NULL,
            password varchar(40) NOT NULL,
            email varchar(255),
            description TEXT,
            embedding BLOB,
            description_en TEXT,
            applied_date varchar(10),
            closed_date varchar(10),
            duration int,
            update_ts DATETIME NOT NULL,
            status varchar(10) NOT NULL,
            timestamp DATETIME NOT NULL
            );
            """)
        extraction_tbl_name = 'uat_extraction' if uat else 'extraction'
        cursor.execute(f"drop table if exists {extraction_tbl_name};")
        cursor.execute(f"""
        create table {extraction_tbl_name}
            (
            id varchar(50) NOT NULL,
            age varchar(20),
            gender varchar(20),
            occupation TEXT,
            marital_status TEXT,
            with_kid varchar(20),
            education TEXT,
            income TEXT,
            nationality TEXT,
            pass TEXT,
            years_sg TEXT,
            years_work TEXT,
            timestamp DATETIME NOT NULL        
            );
            """)
        self.connection.commit()
        return True
    
    @staticmethod
    def md5_hash(string):
        # Create an instance of the MD5 hash object
        md5 = hashlib.md5()
        # Encode the string as bytes and hash it
        md5.update(string.encode('utf-8'))
        # Get the hexadecimal representation of the hash
        hashed_string = md5.hexdigest()
        return hashed_string

    def get_duration(self, applied_date: str, closed_date: str) -> int:
        try:
            t1 = datetime.strptime(applied_date, '%Y-%m-%d')
            t2 = datetime.strptime(closed_date, '%Y-%m-%d')
            duration = (t2 - t1).days
        except:
            duration = -1
        return duration
    
    def connect(self):
        self.connection = mysql.connector.connect(host=self.host, database='sgprapp',
                                            user=self.user,
                                            password=self.password)
    @staticmethod
    def escape_string(x: str) -> str:
        return x.replace("'", "\\'")
    
    def check_user_exist(self, username):
        username = self.escape_string(username)
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"select * from profile where username = '{username}'")
        res = cursor.fetchall()
        if len(res) > 0 :
            return True
        return False

    def add_row(self, username, password, email, status, description, applied_date, closed_date, mode="create", update_ts = '', tablename = 'profile') -> str:
        self.connect()
        cursor = self.connection.cursor()
        sql = f"select * from {tablename} where username = '{self.escape_string(username)}'"
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) > 0 and mode == "create":
            return "user is already existed"
        
        offset = timedelta(hours=8)
        timestamp = (datetime.utcnow() + offset).strftime('%Y-%m-%d %T')  # +8 timezone offset
        update_ts = timestamp if update_ts == '' else update_ts
        id = username + '-' + update_ts
        id_hash = md5_hash(id)
        duration = self.get_duration(applied_date, closed_date)
        description_en = ''
        embedding = ''

        sql = f"""INSERT INTO {tablename} (id, id_hash, username, password, email, description, applied_date, closed_date, 
                    duration, description_en, embedding, update_ts, status, timestamp) 
                       VALUES (
                       \'{self.escape_string(id)}\', \'{id_hash}\',
                       \'{self.escape_string(username)}\', \'{password}\', 
                       \'{email}\', \'{self.escape_string(description)}\',  \'{applied_date}\',  \'{closed_date}\', 
                       \'{duration}\',  \'{self.escape_string(description_en)}\',  \'{embedding}\', 
                       \'{update_ts}\', \'{status}\', \'{timestamp}\');
                       """
        print(sql)
        cursor.execute(sql)
        self.connection.commit()
        self.connection.close()
        return "ok"
    
        
    def verify_user(self, username, password) -> list:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"""
                       select username, email, description, applied_date, closed_date, status from profile 
                       where username = \'{self.escape_string(username)}\' and password = \'{password}\'
                       order by timestamp desc
                       limit 1;
                       """)
        res = cursor.fetchall()
        if len(res) > 0:
            return pd.DataFrame(res, 
                                columns=['username', 'email', 'description', 'applied_date', 'closed_date', 'status']
                                ).to_dict(orient='records')[0]
        return None
        

    def api_fetch_all(self):
        self.connect()
        df = pd.read_sql('select id, username, description,description_en, applied_date, closed_date, duration, update_ts, status from latest order by update_ts desc;', con=self.connection)
        self.connection.close()
        return df.to_dict(orient = 'records')
    

    def update_profile_latest(self):
        self.connect()
        c = self.connection.cursor()
        c.execute('drop table if exists latest;')
        self.connection.commit()
        sql = """
        create table latest as
        (
        select *
        from (select *,
        row_number() over(partition by username order by update_ts desc) as r
        from profile) as ranked
        where r = 1
        order by update_ts desc
        limit 20
        );
        """
        c.execute(sql)
        self.connection.commit()
        self.connection.close()