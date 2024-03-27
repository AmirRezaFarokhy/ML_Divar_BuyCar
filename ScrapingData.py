from bs4 import BeautifulSoup
import urllib3
import pandas as pd
from unidecode import unidecode
import time
import matplotlib.pyplot as plt
import seaborn as sns

from PreprocessingData import Preprocess

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
                           ,',دوررنگ':10,
                          'تمام‌رنگ':10 ,
                         'دوررنگ':10 ,
                         'صافکاری بی‌رنگ':75},
    
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
    time.sleep(5)
    try:
        data = Requests(URL, EXTRACT)
        time.sleep(10)
        all_values_together = []
        cnt = 0
        for a in data.find_all('a', href=True):
            data_path = a['href']
            NEW_URL = PATH + data_path
            time.sleep(10)
            datasets = Requests(NEW_URL, class_type="post-page__section--padded")
            time.sleep(10)
            rows = datasets.findAll('div', 
                        {'class':"kt-base-row kt-base-row--large kt-unexpandable-row"})
            col_row = {}
            token = {}
            for i, row in enumerate(rows):
                key_value = row.get_text(separator=',')
                if i<=1 or key_value.split(',')[1]=='سالم':
                    pass
                elif i==len(rows)-1:
                    col_row['price'] = float(unidecode(key_value.split(',')[1].split(' ')[0]).replace(',', ''))
                    
                elif key_value.split(',')[1]=='شاسی جلو' or key_value.split(',')[1]=='شاسی عقب':
                    token[f'colume_{i}'] = key_value.split(',')[0]
                    col_row[f'colume_{i}'] = key_value.split(',')[1]
                else:
                    token[f'colume_{i}'] = key_value.split(',')[0]
                    col_row[f'colume_{i}'] = key_value.split(',')[1]
                    
            count = 10     
            for conts, keys in zip(datasets.find_all('td')[:-1], datasets.find_all('th')[:-1]):
                col_row[f'colume_{count}'] = int(float(unidecode(conts.contents[0]).replace(',', '')))
                token[f'colume_{count}'] = keys.text
                count += 1

            col_row['url'] = NEW_URL
            if len(col_row)==8:
                cnt += 1
                all_values_together.append(col_row)
                print(f'Done. URL: {NEW_URL}, {cnt}')
            else:
                print(f"\nThis data is less feature so must removed --> {col_row}, leght {len(col_row)}\n")
            if cnt==120:
                break
            

    except Exception as error:
        print("Request is Refus please try again." , error)

    return all_values_together, token



def TokenizationData():
    dataset, token = ExtractDataFromSite()
    for data in dataset:
        for key in data.keys():
            try:
                data[key] = ENV_TOKEN[key][data[key]]
            except Exception as _:
                pass

    for index, data in enumerate(dataset):
        if index==0:
            df = pd.DataFrame([data])
        else:
            df.loc[len(df)] = data 

    return df, token



def VisulizeData(boxplot=False):
    if not boxplot:
        ImportantColumn = ['colume_4', 'colume_6', 'colume_10', 'colume_11', 'colume_3']
        for col in ImportantColumn:
            plt.scatter(df[col], df['price'])
            plt.title("Scatter Plot")
            plt.xlabel(token[col])
            plt.ylabel('Price')
            plt.show()
    else:
        sns.boxplot(df['colume_4'])


dectect_outlier = Preprocess()
df, token = TokenizationData()
main_df = dectect_outlier.RemoveOutliers(df, 'colume_4', 20)
print(f"Dataset is: {df.head()}, Token is: {token}")

# Save data
main_df.to_csv("Cars.csv")


