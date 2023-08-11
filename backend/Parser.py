import os
import openai
openai.organization = "org-oX197NfzZZrGOsEII4Wq3qBh"
openai.api_key =os.getenv("OPENAI_API_KEY") 

from pathlib import Path
import pandas as pd
from tqdm.autonotebook import tqdm
from time import sleep
import json

class GPTParser:

    def __init__(self, parsed_desc_path:str = "", verbose = False):
        self.parsed_desc_path = parsed_desc_path
        self.verbose = verbose
        if parsed_desc_path != "":
            self.init_dirs()
            self.df_parsed = self.get_parsed_dataframe('parsed')
            self.df_embed = self.get_parsed_dataframe('embed')
            self.ex_users = ['admin']

    def init_dirs(self):
        self.parsed_extraction_path = Path(self.parsed_desc_path).joinpath('extraction')
        self.parsed_raw_path = Path(self.parsed_desc_path).joinpath('raw')
        self.parsed_extraction_path.mkdir(parents=True, exist_ok=True)
        self.parsed_raw_path.mkdir(parents=True, exist_ok=True)

    def get_parsed_dataframe(self, type = 'parsed') -> pd.DataFrame:
        if type not in ['parsed', 'embed']:
            raise NotImplementedError
        if type == 'parsed':
            parsed_items = [i.name for i in list(self.parsed_raw_path.glob('*.json'))]
        else:
            parsed_items = [i.name for i in list(Path('./embedding').glob('*.json'))]
        df_parsed = pd.DataFrame({'id': [str(i).replace('.json', '') for i in parsed_items], type: True})
        return df_parsed
        
    def get_unparsed_dataframe(self, data: pd.DataFrame, type = 'parsed') -> pd.DataFrame:
        if type == 'parsed':
            return data.merge(self.df_parsed, on = 'id', how = 'left').fillna({'parsed': False}).query(f"~parsed")
        else:
            return data.merge(self.df_embed, on = 'id', how = 'left').fillna({'embed': False}).query(f"~embed")

    def filter_excluded_users(self, data):
        return data.query("user not in @self.ex_users")
    
    def parse(self, data:pd.DataFrame, type = 'parsed'):
        data = self.filter_excluded_users(data)
        shape_prev = data.shape
        data = self.get_unparsed_dataframe(data, type)
        shape_after = data.shape
        data = data.reset_index(drop=True)
        if self.verbose:
            print(f"{shape_prev[0] - shape_after[0]} records are already {type}.")
            print(f"remaining {shape_after[0]} records are to be {type}.")
        idx = range(len(data))
        pbar = tqdm(idx, total=len(data), desc='extracting', unit='record')
        for i in pbar:
            row = data.iloc[i]
            id = row['id']
            pbar.set_postfix_str(f"{id} | sending")
            text = row['description']
            if type == 'parsed':
                completion = self.get_completion(text)
                pbar.set_postfix_str(f"{id} | saving")
                self.save_completion(completion, id)
            else:
                embeddings = self.get_embedding(text)
                pbar.set_postfix_str(f"{id} | saving")
                self.save_embedding(embeddings, id)
            sleep(1)
        return None


    @staticmethod
    def make_prompt(text:str) -> str:
        prompt = f"""The given text delimited by triple quote, is the description of the immgration application of Singapore Permernant Residency. You are tasked to perform the following task

1. tranlsate into English
2. extract the elements from the translation, return "null" if the element is missing. 
If there're multiple income elements detected, return the max.

Output the result in the following JSON format
{{
    "english_translation": <translation>,
    "extraction": {{
        "age": <age>,
        "gender": <"male" or "female">,
        "occupation": <occupation>,
        "marital_status": <marital status>,
        "with_kid": <whether apply together with kid>,
        "education": <education>,
        "income": <monthly income or salary>,
        "nationality": <nationality>,
        "pass": <current immigration pass>,
        "years_sg": <years in Singapore>,
        "years_work": <years of working>
    }}
}}
Text:\"\"\"{text.strip()}\"\"\""""
        return prompt

    
    def get_completion(self, text:str):
        prompt = self.make_prompt(text)
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = 0,
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
        return completion

    def save_completion(self, completion, id:str):
        filename = f"{id}.json"
        with open(self.parsed_raw_path.joinpath(filename), 'w') as f:
            json.dump(completion, f, indent=2)
        with open(self.parsed_extraction_path.joinpath(filename), 'w') as f:
            f.write(completion.choices[0].message.content)

    @staticmethod
    def flatten_completion(json_file:Path) -> dict:
        with open(json_file, 'r') as f:
            res = json.load(f)
        id = str(json_file.name).replace('.json', '')
        translation = res['english_translation']
        extraction = res['extraction']
        extraction['description_en'] = translation
        extraction['id'] = id
        return extraction
    
    def get_embedding(self, text:str) -> list:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embeddings = response['data'][0]['embedding']
        return embeddings
    
    def save_embedding(self, embeddings:list, id:str):
        with open(f'./embedding/{id}.json', 'w') as f:
            json.dump({id: embeddings}, f, indent=2)
    
    def load_parsed_records(self) -> pd.DataFrame:
        json_files = list(self.parsed_extraction_path.glob("*.json"))
        pbar = tqdm(json_files, total = len(json_files), desc = "combine parsed json files")
        all_res = []
        for json_file in pbar:
            pbar.set_postfix_str(json_file.name)
            try:
                res = self.flatten_completion(json_file)
            except:
                print(json_file)
            all_res += [res]
        return pd.DataFrame(all_res)