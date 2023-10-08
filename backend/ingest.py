import hashlib
import json
from datetime import datetime

class Ingestor:

    def __init__(self, index, parser):
        """
        index: Pinecone Index
        parser: self-defined GPTParser
        """
        self.index = index
        self.parser = parser

    def get_duration(self, applied_date, closed_date) -> int:
        try:
            t1 = datetime.strptime(applied_date, '%Y-%m-%d')
            t2 = datetime.strptime(closed_date, '%Y-%m-%d')
            duration = (t2 - t1).days
        except:
            duration = -1
        return duration

    def md5_hash(self, string) -> str:
        # Create an instance of the MD5 hash object
        md5 = hashlib.md5()

        # Encode the string as bytes and hash it
        md5.update(string.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        hashed_string = md5.hexdigest()

        return hashed_string


    def ingest(self, userid: str, text: str, result: str, applied_date: str, closed_date: str, update_time) -> dict:
        userid = self.md5_hash(userid)
        completion = self.parser.get_completion(text)
        completion_dict = json.loads(str(completion.choices[0].message.content))
        embedding = self.parser.get_embedding(text)
        duration = self.get_duration(applied_date, closed_date)
        metadata = {
            'desc': text,
            'desc_en': completion_dict['english_translation'],
            'result': result,  # pass | rejected | pending
            'duration': duration,  # in # days
            'update_time': update_time}
        extraction = completion_dict['extraction']
        extraction = {"extracted_" + k: v for k,
                    v in extraction.items() if v is not None}

        payload = (userid, embedding, metadata | extraction)
        self.index.upsert([payload])
        print(f'id [{userid}] ingested:  {text}')
        return payload