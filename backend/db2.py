import hashlib
from datetime import datetime, timedelta
import psycopg

def md5_hash(string):
    # Create an instance of the MD5 hash object
    md5 = hashlib.md5()
    # Encode the string as bytes and hash it
    md5.update(string.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    hashed_string = md5.hexdigest()
    return hashed_string

class DB:
    def __init__(self,  password, host= 'db.prvpwciugakwrbsdbsoa.supabase.co', user='postgres'):
        self.host = host
        self.user = user
        self.password = password
        self.port = 5432
        # self.schema = schema = 'sgprapp'
        # self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{schema}', echo = False)
        self.connection = psycopg.connect(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/postgres', autocommit=True)
        # print(self.connection.get_server_info())
        self.connection.close()
        self.record_cols = ['id','username', 'email', 'description', 'description_en','applied_date', 'closed_date', 'update_ts','status', 'duration']
        self.record_cols_string = ', '.join(self.record_cols)

    @staticmethod
    def add_cols(db_out: list, cols: list):
        return [dict(zip(cols, o)) for o in db_out]

    def connect(self):
        if self.connection.closed:
            self.connection = psycopg.connect(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/postgres', autocommit=True)
        
    def initdb(self, uat = False) -> bool:
        
        tablename = 'uat_profile' if uat else 'profile'
        self.execute_sql(f"drop table if exists {tablename};")
        sql = f"""
        create table {tablename} 
            (
            id TEXT NOT NULL,
            id_hash TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            description TEXT,
            embedding VECTOR(1536),
            description_en TEXT,
            applied_date DATE,
            closed_date DATE,
            duration INT8,
            update_ts TIMESTAMP NOT NULL,
            status TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
            );
            """
        self.execute_sql(sql)
        extraction_tbl_name = 'uat_extraction' if uat else 'extraction'

        self.execute_sql(f"drop table if exists {extraction_tbl_name};")
        sql = f"""
        create table {extraction_tbl_name}
            (
            id TEXT NOT NULL,
            age TEXT,
            gender TEXT,
            occupation TEXT,
            marital_status TEXT,
            with_kid TEXT,
            education TEXT,
            income TEXT,
            nationality TEXT,
            pass TEXT,
            years_sg TEXT,
            years_work TEXT,
            timestamp DATETIME NOT NULL        
            );
            """
        self.execute_sql(sql)
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
    

    @staticmethod
    def escape_string(x: str) -> str:
        return x.replace("'", "\\'")
    
    def check_user_exist(self, username) -> bool:
        username = self.escape_string(username)
        res = self.execute_sql(f"select * from profile where username = '{username}'", return_result=True)
        if len(res) > 0 :
            return True
        return False
    
    def add_row(self, username, password, email, status, description, applied_date, closed_date, mode="create", update_ts = '', tablename = 'profile') -> dict:
  
        sql = f"select * from {tablename} where username = '{self.escape_string(username)}'"
        # print(sql)
        res = self.execute_sql(sql, return_result=True)
        if len(res) > 0 and mode == "create":
            return {'status': "user is already existed"}
        
        offset = timedelta(hours=8)
        timestamp = (datetime.utcnow() + offset).strftime('%Y-%m-%d %T')  # +8 timezone offset
        update_ts = timestamp if update_ts == '' else update_ts
        id = username + '-' + update_ts
        id_hash = md5_hash(id)
        duration = self.get_duration(applied_date, closed_date)
        description_en = ''
        # embedding = ''

        sql = f"""INSERT INTO {tablename} (id, id_hash, username, password, email, description, description_en, applied_date, closed_date, 
                    duration, update_ts, status, timestamp) 
                       VALUES (
                       \'{self.escape_string(id)}\', \'{id_hash}\',
                       \'{self.escape_string(username)}\', \'{password}\', 
                       \'{email}\', \'{self.escape_string(description)}\', '{description_en}' ,\'{applied_date}\',  \'{closed_date}\', 
                       \'{duration}\',  
                       \'{update_ts}\', \'{status}\', \'{timestamp}\');
                       """
        # print(sql)
        self.execute_sql(sql)
        return {'status':'ok', 'id': id}
    
    def update_record(self, id, status, description, applied_date, closed_date,  update_ts = '', tablename = 'profile') -> dict:
        sql = f"""update {tablename} 
        set status = '{status}', 
        description = '{description}',
        applied_date = '{applied_date}',
        closed_date = '{closed_date}',
        update_ts = '{update_ts},'
        description_en = '',
        embedding = ''
        where id = '{id}';
        """
        self.execute_sql(sql)
        return {'status': 'ok'}
        
    def verify_user(self, username, password) -> dict:
        sql = f"""
        select {self.record_cols_string} from profile 
        where username = \'{self.escape_string(username)}\' and password = \'{password}\'
        order by timestamp desc
        limit 1;
        """
        res = self.execute_sql(sql, return_result=True)
        res = self.add_cols(res, self.record_cols)
        if len(res) > 0:
            return  {'status': 'ok', 'record':res[0]}
        return {'status': 'wrong username and passowrd combination'}
    
    def api_fetch_all(self) -> list:
        sql = f'select {self.record_cols_string} from latest order by update_ts desc;'
        out = self.execute_sql(sql, return_result=True)
        out = self.add_cols(out, self.record_cols)
        return out
    
    def execute_sql(self, sql, return_result = False) -> list:
        self.connect()
        c = self.connection.cursor()
        c.execute(sql)
        self.connection.commit()
        if return_result:
            return c.fetchall()
        else:
            return []
    
    def list_user_records(self, username) -> list[dict]:

        sql = f"""select {self.record_cols_string} from profile where username = '{self.escape_string(username)}'"""
        res = self.execute_sql(sql, return_result=True)
        res = self.add_cols(res, self.record_cols)
        return res

    def update_profile_latest(self):     
        self.execute_sql('drop table if exists latest;')
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
        self.execute_sql(sql)
        self.connection.close()

    def get_similar_from_embedding(self, emb: list[float]) -> list:
        cols = self.record_cols + ['distance']
        sql = f"""select 
        {self.record_cols_string},
        embedding <=> '{emb}' as distance
        from profile
        where status in ('pass', 'rejected') and duration > 0
        order by embedding <=> '{emb}'
        limit 5;
        """
        res = self.execute_sql(sql, return_result=True)
        return self.add_cols(res, cols)
    
    def upload_extraction(self, id: str, extraction: dict) -> None: 
        extraction_slim = {k:v for k,v in extraction.items() if v is not None}
        if len(extraction_slim) > 0:
            cols = ", ".join(extraction_slim.keys())
            values = ", ".join([self.escape_string(i) for i in extraction_slim.values()])
            sql = f"""insert into extraction (id, {cols})
                values (
                    '{self.escape_string(id)}',  '{values}'
                );
                """
            self.execute_sql(sql)

    def update_completion(self, id: str, emb: list, description_en: str):
        sql = f"update profile set embedding = '{emb}', description_en = '{self.escape_string(description_en)}' where id = '{self.escape_string(id)}';"
        # print(sql)
        self.execute_sql(sql)
        return True

    def delete_records(self, ids: list[str]) -> bool:
        ids = [f"'{self.escape_string(i)}'" for i in ids]
        id_string = f"({', '.join(ids)})"
        sql = f"delete from profile where id in {id_string};"
        self.execute_sql(sql)
        sql = f"delete from latest where id in {id_string};"
        self.execute_sql(sql)
        return True