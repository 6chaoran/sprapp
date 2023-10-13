from pathlib import Path
import pandas as pd
import json
from openai.openai_object import OpenAIObject
import numpy
import io
import hashlib
from datetime import datetime

class BatchIngestor:

    def __init__(self, parser, engine, maria, index, uat) -> None:
        self.parser = parser
        self.engine = engine
        self.maria = maria
        self.index = index
        self.maria.connect()
        self.uat = uat

    @staticmethod
    def impute_update_ts(row: pd.Series) -> str:
        update_ts = row.update_ts
        closed_date = row.closed_date
        applied_date = row.applied_date
        if not isinstance(update_ts, str):
            if not isinstance(closed_date, str):
                return applied_date
            else:
                return closed_date
        else:
            return update_ts
        
    @staticmethod
    def impute_username(x: str) -> str:
        return 'dummy' if x == None else str(x)

    @staticmethod
    def is_datestring_valid(x: str, format = '%Y-%m-%d'):
        try:
            datetime.strptime(x, format)
            return True
        except:
            return False
        
    def impute_datestring(self, x: str, format = '%Y-%m-%d'):
        if self.is_datestring_valid(x, format):
            return x
        else:
            return None
        
    def confirmed_status_invalid_closed_date(self, row):
        closed_date = row.closed_date
        status = row.status
        return (not self.is_datestring_valid(closed_date)) and status in ['pass', 'rejected']
        
    def preprocess(self, df):
        _RESULT_MAP = {
            '等待': 'pending',
            '通过': 'pass',
            '批准': 'pass',
            '杯具': 'rejected',
            '失败': 'rejected',
            '进行中': 'pending',
            '上诉中': 'rejected'
        }
        _RENAME_MAP = {
            'user': 'username', 
            'result': 'status', 
            'apply_dt': 'applied_date', 
            'close_dt': 'closed_date'
            }
        df_copy = df.drop(columns=['Col1']).rename(columns = _RENAME_MAP)
        df_copy['status'] = df_copy['status'].map(lambda x: _RESULT_MAP.get(x, x))
        df_copy['applied_date'] = df_copy['applied_date'].map(self.impute_datestring)
        df_copy['closed_date'] = df_copy['closed_date'].map(self.impute_datestring)
        df_copy['username'] = df_copy['username'].map(self.impute_username)
        df_copy['update_ts'] = df_copy.apply(self.impute_update_ts, axis = 1)
        df_copy['id'] = df_copy.apply(lambda row: str(row['username']) + '-' + str(row['update_ts']), axis = 1)
        # filter out short reviews
        df_copy = df_copy.loc[df_copy['description'].map(lambda x: len(str(x)) >= 10), :]
        # ensure valid status
        df_copy = df_copy.loc[df_copy['status'].isin(['pass', 'pending', 'rejected']), :]
        # ensure valid date
        df_copy = df_copy.loc[df_copy['applied_date'].map(lambda x: x != None), :]
        df_copy = df_copy.loc[~df_copy.apply(self.confirmed_status_invalid_closed_date, axis = 1),:]
        return df_copy
        
    def get_df_delta(self):

        uat = self.uat
        p = Path('./extract')
        res = []
        for d in p.glob('pr/*.csv'):
            res += [pd.read_csv(d)]
        df_all = pd.concat(res)
        df_all = self.preprocess(df_all)

        tbl_name = 'uat_profile' if uat else 'profile'
        df_latest = pd.read_sql(f'select unique id from {tbl_name};', con = self.maria.connection)
        ids = df_latest['id']
        df_delta = df_all.query('id not in @ids')
        print(df_delta.shape)
        return df_delta
    
    @staticmethod
    def completion_to_dict(completion: OpenAIObject) -> dict:
        try:
            res = json.loads(completion.choices[0].message.content, strict = False)
        except:
            res = {'english_translation': 'Apologies, something wrong with the translation', 
                'extraction': {}}
        return res
    
    @staticmethod
    def adapt_array(array):
        """
        Using the numpy.save function to save a binary version of the array,
        and BytesIO to catch the stream of data and convert it into a BLOB.
        """
        out = io.BytesIO()
        numpy.save(out, array)
        out.seek(0)

        return out.read()
    
    @staticmethod
    def convert_array(blob):
        """
        Using BytesIO to convert the binary version of the array back into a numpy array.
        """
        out = io.BytesIO(blob)
        out.seek(0)

        return numpy.load(out)

    @staticmethod
    def get_duration(applied_date, closed_date) -> int:
        try:
            t1 = datetime.strptime(applied_date, '%Y-%m-%d')
            t2 = datetime.strptime(closed_date, '%Y-%m-%d')
            duration = (t2 - t1).days
        except:
            duration = -1
        return duration

    @staticmethod
    def md5_hash(string) -> str:
        # Create an instance of the MD5 hash object
        md5 = hashlib.md5()
        # Encode the string as bytes and hash it
        md5.update(string.encode('utf-8'))
        # Get the hexadecimal representation of the hash
        hashed_string = md5.hexdigest()
        return hashed_string


    def _prepare_row_upload(self, row: pd.Series, embedding: list) -> pd.DataFrame:
        df_row = pd.DataFrame([row])
        df_row['password'] = '123'
        df_row['timestamp'] = datetime.now()
        df_row['embedding'] = self.adapt_array(embedding)
        return df_row

    @staticmethod
    def _prepare_extraction_upload(extraction: dict) -> pd.DataFrame:
        df_extraction = pd.DataFrame([extraction])
        df_extraction['timestamp'] = datetime.now()
        return df_extraction

    def _prepare_vectordb_row(self, row: pd.Series, res, embedding) -> tuple[str, list, dict]:
        uat = self.uat
        metadata = {
        'desc': row.description,
        'desc_en': row.description_en,
        'result': row.status,
        'duration': row.duration,
        'update_time': row.update_ts,
        'uat': uat
        } 
        
        extraction = res.get('extraction', {})
        if len(extraction) > 0:
            extra = {"extracted_" + k: v for k,
                            v in extraction.items() if v is not None}
            metadata = metadata | extra
            
        id = row.id_hash
        payload = (id, embedding, metadata)
        return payload

    @staticmethod
    def escape_string(x: str) -> str:
        return x.replace("'", "\\'")

    def upload_to_db(self, row: pd.Series, completions: OpenAIObject = None, embedding: list = []) -> None:
        """upload to database:
        index: Pinecone index
        """
        uat = self.uat
        tbl_name_extraction = 'uat_extraction' if uat else 'extraction'
        tbl_name_profile = 'uat_profile' if uat else 'profile'

        row['duration'] = self.get_duration(row.applied_date, row.closed_date)
        row['id_hash'] = self.md5_hash(row.id)

        if completions:
            res = self.completion_to_dict(completions)
            row['description_en'] = res.get('english_translation')
            extraction = {'id': row.id} | res.get('extraction', {})
            df_extraction = self._prepare_extraction_upload(extraction)
        else:
            row['description_en'] = row.description
            
        df_row = self._prepare_row_upload(row, embedding)
        
        # upload to MySQL
        self.maria.connect()
        c = self.maria.connection.cursor()
        c.execute(f"delete from {tbl_name_profile} where id = \'{self.escape_string(row.id)}\'")
        self.maria.connection.commit()
        df_row.to_sql(tbl_name_profile, con = self.engine, if_exists='append', index = False)
        self.maria.connection.commit()

        if completions:
            c.execute(f"delete from {tbl_name_extraction} where id = \'{self.escape_string(row.id)}\'")
            self.maria.connection.commit()
            df_extraction.to_sql(tbl_name_extraction, con=self.engine, if_exists='append', index=False)
            self.maria.connection.commit()
            if row['status'] in ['pass', 'rejected'] and len(str(row['description']).strip()) >= 10:
                # upload to PineCone
                payload = self._prepare_vectordb_row(row, res, embedding)
                self.index.upsert([payload], namespace = 'spr')

    def ingest_row(self, row: pd.Series) -> None:
        description = str(row.description).strip()
        if len(description) >= 10:
            completions = self.parser.get_completion(row.description)
        else:
            completions = None
        embedding = self.parser.get_embedding(row.description)
        self.upload_to_db(row, completions, embedding)


if __name__ == '__main__':
    from tqdm import tqdm
    from time import sleep
    # init mysql
    import pandas as pd
    import mysql.connector
    from sqlalchemy import create_engine

    user = 'chaoran'
    password = '100200'
    host = '192.168.31.141'
    port = 3306
    schema = 'sgprapp'
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{schema}', echo = False)

    from backend.db import DB
    maria = DB(host, user, password)
    maria.connect()

    # init OPENAI LLM
    from backend.Parser import GPTParser
    parser = GPTParser()

    # init pinecone
    import pinecone
    import os
    PINECONE_API_KEY =  os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT") 
    pinecone.init(api_key=PINECONE_API_KEY,
                environment=PINECONE_ENVIRONMENT)
    index = pinecone.Index('spr')

    uat = False

    ingestor = BatchIngestor(parser, engine, maria, index, uat)

    df_delta = ingestor.get_df_delta()

    progress_bar = tqdm(range(len(df_delta)), desc='ingesting', unit='record')
    for i in progress_bar:
        row = df_delta.iloc[i]
        progress_bar.set_postfix_str(f'[{row.id}]')
        try:
            ingestor.ingest_row(row)
        except Exception as e:
            print(e)
            progress_bar.set_postfix_str('waiting')
            sleep(60)
            progress_bar.set_postfix_str(f'[{row.id}]')
            ingestor.ingest_row(row)
    print('update the latest table')
    maria.update_profile_latest()
    maria.connection.close()