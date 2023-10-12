from pathlib import Path

import scrapy
import pandas as pd
import csv
from datetime import datetime

class SCSpider(scrapy.Spider):
    name = "sc"
    def __init__(self):
        super().__init__()
        self.tbl_header = ['Col1','user','description', 'result','apply_dt','close_dt','update_ts']        
        self.today = f'{datetime.today():%Y-%m-%d}'
        self.pages = 1

    def start_requests(self):

        urls = [
            'http://sgprapp.com/citizen?page=0'
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = []
        rows = response.xpath('//*[@id="myTable"]/tbody/tr')
        for row in rows:
            fields = row.xpath('td')
            row_data = [f.xpath('text()').get('null') for f in fields]
            row_data = [str(i).strip() for i in row_data]
            row_dict = dict(zip(self.tbl_header, row_data))
            data += [row_dict]

        data_df = pd.DataFrame(data)
        page = response.url.split("=")[-1]
        filename = f'sc-page-{page}.csv'
        filepath = Path(f'../extract/{self.today}/sc')
        filepath.mkdir(parents=True, exist_ok=True)
        data_df.to_csv(filepath.joinpath(filename), index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        self.log(f'Saved file {filename}')

        next_page = response.xpath('//a[text()="下一页"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)