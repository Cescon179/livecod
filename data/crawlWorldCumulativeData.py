import requests, re, json, csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

confirmed_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
deaths_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
recovered_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

confirmed_total_data = []
deaths_total_data = []
recovered_total_data = []

with requests.Session() as s:
    download = s.get(confirmed_CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        confirmed_total_data.append(row)

with requests.Session() as s:
    download = s.get(deaths_CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        deaths_total_data.append(row)

with requests.Session() as s:
    download = s.get(recovered_CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        recovered_total_data.append(row)

# confirmed_total_data[0]
confirmed_df = pd.DataFrame(confirmed_total_data[1:], columns=confirmed_total_data[0])
deaths_df = pd.DataFrame(deaths_total_data, columns=deaths_total_data[0])
recovered_total_data = pd.DataFrame(recovered_total_data, columns=recovered_total_data[0])

confirmed_cols = confirmed_df.columns[confirmed_df.columns.str.endswith('20')]

confimred_result = pd.DataFrame()
confirmed_result = confirmed_df.filter(confirmed_cols, axis=1)
confirmed_result = confirmed_result.astype(int)

confirmed_result.loc['Total Confimred'] = confirmed_result.sum()
confirmed_result = confirmed_result.tail(1)


confirmed_result.columns = range(confirmed_result.shape[1])
confirmed_result = list(confirmed_result.iloc[0])

print(confirmed_result)

death_cols = deaths_df.columns[deaths_df.columns.str.endswith('20')]

deaths_result = pd.DataFrame()
deaths_result = deaths_df.filter(death_cols, axis=1)
deaths_result = deaths_result.drop(deaths_result.index[0])
deaths_result = deaths_result.astype(int)

deaths_result.loc['Total Deaths'] = deaths_result.sum()
deaths_result = deaths_result.tail(1)
deaths_result.columns = range(deaths_result.shape[1])
deaths_result = list(deaths_result.iloc[0])
print(deaths_result)

recover_cols = recovered_total_data.columns[recovered_total_data.columns.str.endswith('20')]

recover_result = pd.DataFrame()
recover_result = recovered_total_data.filter(recover_cols, axis=1)
recover_result = recover_result.iloc[1:]
#recover_result = recover_result.drop(new_recover_df.index[0])
recover_result = recover_result.astype(int)

#날짜계산
date = recover_result.head()

recover_result.loc['Total recovery'] = recover_result.sum()
recover_result = recover_result.tail(1)
recover_result.columns = range(recover_result.shape[1])

recover_result = list(recover_result.iloc[0])
print(recover_result)

date = [ i[:-3] for i in date ]

resultData = list(zip(date, confirmed_result, deaths_result, recover_result))

with open("./data/worldCumulativeData.js", "w", encoding='UTF-8-sig') as json_file:
    json.dump(resultData, json_file, ensure_ascii=False, indent=4)

data = ''
with open("./data/worldCumulativeData.js", "r", encoding='UTF-8-sig') as f:
    while True:
        line = f.readline()
        if not line: break
        data += line
data = '//Auto-generated by crawlWorldCumulativeData.py\nvar crawlWorldCumulativeData = ' + data + ';'

with open("./data/worldCumulativeData.js", "w", encoding='UTF-8-sig') as f_write:
    f_write.write(data)
