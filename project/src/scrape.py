import os
import requests
import pandas
from requests_html import HTML

THIS_FILE = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(THIS_FILE)
CSV_DIR=os.path.join(BASE_DIR,'data')


def url_to_csv(*, url: str, save: bool = True):

    data=[]
    
    request = requests.get(url)
    if request.status_code == 200:
        result = request.text
        
        #Html tranform
        #Salón fama #PLHoF

        r_thml = HTML(html=result)
        table_class = '#top20'
        r_table = r_thml.find(table_class)
        parsed_table = r_table[0]

        rows = parsed_table.find('tr')

        headers_name=parsed_table.find('th')
        headers = [header.text for header in headers_name]
        for row in rows[1:]:
            row_data = []
            cols = row.find('td')
            for col in cols:
                row_data.append(col.text)
        
            data.append(row_data)
        
        if save:
            if not os.path.isdir(CSV_DIR):
                os.makedirs(CSV_DIR)
            
            filename=os.path.join(CSV_DIR,'tiobeScrapping.csv')
            data_frame = pandas.DataFrame(data, columns=headers)
            data_frame.to_csv(filename, index=False)

        return data

url='https://www.tiobe.com/tiobe-index/'
url_to_csv(url=url)
