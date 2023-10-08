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
        df_copy['update_ts'] = df_copy.apply(self.impute_update_ts, axis = 1)
        df_copy['id'] = df_copy.apply(lambda row: str(row['username']) + '-' + str(row['update_ts']), axis = 1)
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


    def upload_to_db(self, row: pd.Series, completions: OpenAIObject, embedding: list) -> None:
        """upload to database:
        index: Pinecone index
        """
        uat = self.uat
        tbl_name_extraction = 'uat_extraction' if uat else 'extraction'
        tbl_name_profile = 'uat_profile' if uat else 'profile'
        res = self.completion_to_dict(completions)
        row['description_en'] = res.get('english_translation')
        row['duration'] = self.get_duration(row.applied_date, row.closed_date)
        row['id_hash'] = self.md5_hash(row.id)

        extraction = {'id': row.id} | res.get('extraction', {})
        
        df_row = self._prepare_row_upload(row, embedding)
        df_extraction = self._prepare_extraction_upload(extraction)

        # upload to MySQL
        df_row.to_sql(tbl_name_profile, con = self.engine, if_exists='append', index = False)
        self.maria.connection.commit()
        df_extraction.to_sql(tbl_name_extraction, con=self.engine, if_exists='append', index=False)
        self.maria.connection.commit()

        # upload to PineCone
        payload = self._prepare_vectordb_row(row, res, embedding)
        index.upsert([payload])


    def ingest_row(self, row: pd.Series) -> None:
        embedding = self.parser.get_embedding(row.description)
        completions = self.parser.get_completion(row.description)
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
    engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}:{port}/{schema}', echo = False)

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

    uat = True

    ingestor = BatchIngestor(parser, engine, maria, index, uat)

    df_delta = ingestor.get_df_delta()

    progress_bar = tqdm(range(len(df_delta)), desc='ingesting', unit='record')
    for i in progress_bar:
        row = df_delta.iloc[i]
        progress_bar.set_postfix_str(f'[{row.id}]')
        try:
            ingestor.ingest_row(row)
            sleep(2)
        except Exception as e:
            print(e)
            progress_bar.set_postfix_str('waiting')
            sleep(60)
            progress_bar.set_postfix_str(f'[{row.id}]')
            ingestor.ingest_row(row)

