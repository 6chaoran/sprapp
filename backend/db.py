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

    def initdb(self, uat = False) -> bool:
        self.connect()
        cursor = self.connection.cursor()
        tablename = 'uat_profile' if uat else 'profile'
        cursor.execute(f"drop table if exists {tablename};")
        # cursor.execute(f"""
        # create table {tablename} 
        #     (
        #     id int AUTO_INCREMENT PRIMARY KEY,
        #     username varchar(40) NOT NULL,
        #     password varchar(40) NOT NULL,
        #     email varchar(255) NOT NULL,
        #     description TEXT NOT NULL,
        #     applied_date varchar(10),
        #     closed_date varchar(10),
        #     timestamp DATETIME NOT NULL,
        #     status varchar(10) NOT NULL
        #     );
        #     """)
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

    def connect(self):
        self.connection = mysql.connector.connect(host=self.host, database='sgprapp',
                                            user=self.user,
                                            password=self.password)
        
    def add_row(self, username, password, email, status, description, applied_date, closed_date, mode="create", update_ts = '', tablename = 'profile') -> str:
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f"select * from {tablename} where username = \'{username}\'")
        res = cursor.fetchall()
        if len(res) > 0 and mode == "create":
            return "user is already existed"
        
        update_ts = datetime.now().strftime('%Y-%m-%d %T') if update_ts == '' else update_ts

        cursor.execute(f"""
                       INSERT INTO {tablename} (username, password, email, description, applied_date, closed_date, timestamp, status) 
                       VALUES (
                       \'{username}\', \'{password}\', 
                       \'{email}\', \'{description}\',  \'{applied_date}\',  \'{closed_date}\', 
                       \'{update_ts}\', \'{status}\');
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
        
    def fetch_all(self, nrows = 0, tablename = 'profile_latest'):
        self.connect()
        cursor = self.connection.cursor()
        # cursor.execute('select id, username, description, timestamp, status, applied_date, closed_date from profile order by timestamp desc;')
        cursor.execute(f'select id, username, description, timestamp, status, applied_date, closed_date from {tablename} order by timestamp desc;')
        df = pd.DataFrame(cursor.fetchall(), columns=['id','username', 'description', 'timestamp','status', 'applied_date', 'closed_date'])
        self.connection.close()
        # df = pd.DataFrame(df, columns=['id','username', 'description', 'datetime','status', 'applied_date', 'closed_date'])
        # df['rank'] = df.groupby('username', as_index = False)['datetime'].rank(ascending=False)
        # df = df.query("rank == 1")
        if nrows > 0:
            df = df[:nrows]
        return df.to_dict(orient='records')
    

    def update_profile_latest(self, tablename = 'profile_latest'):
        self.connect()
        cursor = self.connection.cursor()
        sqltext=f"""
        drop table if exists {tablename};
        """
        cursor.execute(sqltext)
        self.connection.commit()

        sqltext = f"""
        create table {tablename} as
        select 
        id, username, password,email, description, applied_date, closed_date, timestamp, status 
        from 
        (
            select *, 
            dense_rank() over(partition by username order by timestamp desc) as rank 
            from profile
        ) as ranked
        where rank = 1
        order by timestamp desc
        limit 10;
        """
        cursor.execute(sqltext)
        self.connection.commit()
