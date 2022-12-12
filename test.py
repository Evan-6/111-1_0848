import requests
import json


url = "https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4051&limited=TWN"
response = requests.get(url)
data = json.loads(response.text)
for i in data:
    print(i.get('a04'),i.get('a06'))