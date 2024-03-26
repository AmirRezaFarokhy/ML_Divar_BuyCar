from bs4 import BeautifulSoup
import urllib3
import pandas as pd
from unidecode import unidecode
import time

# ASK = input("What type of car you want? ")
# PATH = 'https://divar.ir'
# URL = f'{PATH}/s/iran/auto?q={ASK}'
# EXTRACT = "post-list__items-container-e44b2"


PATH = "https://divar.ir"
URL = f"{PATH}/s/iran/auto?q=206"
EXTRACT = "post-list__items-container-e44b2"
ENV_TOKEN = {
            'colume_4' : {'خط و خش جزیی':85
                           ,'رنگ‌شدگی':45
                           ,'سالم و بی‌خط و خش':100 
                           ,'دوررنگ':10},
             'colume_3' : {'سالم و پلمپ':90, 
                           'ضربه‌خورده':10},
             'colume_6' : {'اتوماتیک':1, 
                           'دنده\u200cای':0}
}



def Requests(path_req, class_type=None):
    req = urllib3.PoolManager()
    res = req.request('GET', path_req)
    soup = BeautifulSoup(res.data, 'html.parser')
    data = soup.findAll('div', {'class':class_type})[0]
    return data


def ExtractDataFromSite():
    time.sleep(2)
    try:
        data = Requests(URL, EXTRACT)
        time.sleep(8)
        all_values_together = []
        for d in data.findAll('div', {'class':"post-list__widget-col-c1444"}):
            for a in d.find_all('a', href=True):
                data_path = a['href']
                NEW_URL = PATH + data_path
                time.sleep(60)
                datasets = Requests(NEW_URL, class_type="post-page__section--padded")
                time.sleep(30)
                rows = datasets.findAll('div', 
                            {'class':"kt-base-row kt-base-row--large kt-unexpandable-row"})
                col_row = {}
                token = {}
                for i, row in enumerate(rows):
                    key_value = row.get_text(separator=',')
                    if i<=1:
                        pass
                    elif key_value.split(',')[1]=='سالم':
                        pass
                    elif i==len(rows)-1:
                        col_row['price'] = float(unidecode(key_value.split(',')[1].split(' ')[0]).replace(',', ''))
                    elif i==5:
                        token[f'colume_{i}'] = key_value.split(',')[0]
                        col_row[f'colume_{i}'] = int(unidecode(key_value.split(',')[1].split(' ')[0]))
                    else:
                        token[f'colume_{i}'] = key_value.split(',')[0]
                        col_row[f'colume_{i}'] = key_value.split(',')[1]
                count = 10     
                for conts, keys in zip(datasets.find_all('td')[:-1], datasets.find_all('th')[:-1]):
                    col_row[f'colume_{count}'] = int(unidecode(conts.contents[0]).replace(',', ''))
                    token[f'colume_{count}'] = keys.text
                    count += 1

                col_row['url'] = NEW_URL
                all_values_together.append(col_row)
                print(f'Done. URL: {NEW_URL}')
            
    except Exception as error:
        print("Request is Refus please try again." , error)

    return all_values_together, token



def TokenizationData():
    dataset, token = ExtractDataFromSite()
    for data in dataset:
        for key in data.keys():
            try:
                data[key] = ENV_TOKEN[key][data[key]]
            except Exception as cannot:
                pass
    return dataset, token


def CreateDataFrame():
    dataset, token = TokenizationData()
    for index, data in enumerate(dataset):
        if index==0:
            df = pd.DataFrame([data])
        else:
            df.loc[len(df)] = data 
    
    return df, token


df, token = CreateDataFrame()

print(f"Dataset is: {df.head()}, Token is: {token}")



