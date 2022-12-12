import requests
import json


url = "https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4051&limited=TWN"
response = requests.get(url)
data = json.loads(response.text)
# print(data)
url = "https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4051&limited=TWN"
response = requests.get(url)
data = json.loads(response.text)
month = '01'
numsum = 0
plot_numlist=[]
for i in data:
    if month=='11':
        break
    data_month = i.get('a04').split('-')[1]
    data_num = i.get('a06')
    if month==data_month:
        numsum += int(data_num)
    else:
        # print(month , numsum)
        plot_numlist.append(numsum)
        month = data_month
        numsum = 0

print(plot_numlist)