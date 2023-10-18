from backend.db2 import DB
import os
db = DB(os.getenv('SUPABASE_PASSWORD'))

# init OPENAI LLM
from backend.Parser import GPTParser
parser = GPTParser()

from pathlib import Path
import pandas as pd
from datetime import datetime
from tqdm import tqdm

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

def impute_username(x: str) -> str:
    return 'dummy' if x == None else str(x)

def is_datestring_valid(x: str, format = '%Y-%m-%d'):
    try:
        datetime.strptime(x, format)
        return True
    except:
        return False
    
def impute_datestring(x: str, format = '%Y-%m-%d'):
    if is_datestring_valid(x, format):
        return x
    else:
        return None
    
def confirmed_status_invalid_closed_date(row):
    closed_date = row.closed_date
    status = row.status
    return (not is_datestring_valid(closed_date)) and status in ['pass', 'rejected']
    
def preprocess(df):
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
        df_copy['applied_date'] = df_copy['applied_date'].map(impute_datestring)
        df_copy['closed_date'] = df_copy['closed_date'].map(impute_datestring)
        df_copy['username'] = df_copy['username'].map(impute_username)
        df_copy['update_ts'] = df_copy.apply(impute_update_ts, axis = 1)
        df_copy['id'] = df_copy.apply(lambda row: str(row['username']) + '-' + str(row['update_ts']), axis = 1)
        # filter out short reviews
        df_copy = df_copy.loc[df_copy['description'].map(lambda x: len(str(x)) >= 10), :]
        # ensure valid status
        df_copy = df_copy.loc[df_copy['status'].isin(['pass', 'pending', 'rejected']), :]
        # ensure valid date
        df_copy = df_copy.loc[df_copy['applied_date'].map(lambda x: x != None), :]
        df_copy = df_copy.loc[~df_copy.apply(confirmed_status_invalid_closed_date, axis = 1),:]
        return df_copy

def get_df_delta():

    p = Path('./extract')
    res = []
    for d in p.glob('pr/*.csv'):
        res += [pd.read_csv(d)]
    df_all = pd.concat(res)
    df_all = preprocess(df_all)
    db.connect()
    df_latest = pd.read_sql(f'select distinct id from profile;', con = db.connection)
    db.connection.close()
    ids = df_latest['id']
    df_delta = df_all.query('id not in @ids')
    print(df_delta.shape)
    return df_delta

def ingest(id, text):
    emb = parser.get_embedding(text)
    completion = parser.get_completion(text)
    compl_dict = parser.completion_to_dict(completion)
    extraction = compl_dict.get('extraction', {})
    description_en = compl_dict.get('english_translation', 'Apologies, something wrong with the translation')
    db.update_completion(id, emb, description_en)
    db.upload_extraction(id, extraction)


if __name__ == "__main__":

    df_delta = get_df_delta()
    progress_bar = tqdm(range(len(df_delta)), desc='ingesting', unit='record')
    for i in progress_bar:
        row = df_delta.iloc[i]
        progress_bar.set_postfix_str(f'[{row.id}]')
        id = row.username + '-' + row.update_ts
        db.add_row(row.username, 
                password='123', 
                email='6chaoran@gmail.com', 
                status = row.status, 
                description=row.description, 
                applied_date=row.applied_date, 
                closed_date=row.closed_date, 
                update_ts=row.update_ts,
                mode= 'edit'
                )
        
        ingest(id, row.description)

    db.update_profile_latest()