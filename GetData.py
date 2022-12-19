import requests
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv
import xmltodict

time = ["2022/01","2022/02","2022/03","2022/04","2022/05","2022/06","2022/07","2022/08","2022/09","2022/10"]
if __name__ == '__main__':

#台中#######################################################################################################################
    # data source : https://data.gov.tw/dataset/146920
    taichung_data_url_list={
        '2022/10':'https://datacenter.taichung.gov.tw/swagger/OpenData/052ba9b8-040b-42be-a3c8-dcc96324cfc8',
        '2022/09':'https://datacenter.taichung.gov.tw/swagger/OpenData/95ac9ad4-4b36-41c9-9937-68a9834c7687',
        '2022/08':'https://datacenter.taichung.gov.tw/swagger/OpenData/13059e7b-541e-45cf-8484-9c2b0992f640',
        '2022/07':'https://datacenter.taichung.gov.tw/swagger/OpenData/51de8f68-ca12-4026-be5d-1e58f2c695bd',
        '2022/06':'https://datacenter.taichung.gov.tw/swagger/OpenData/cee7c8f7-6044-4857-af38-b8e6bdd3f352',
        '2022/05':'https://datacenter.taichung.gov.tw/swagger/OpenData/7d9ac916-3891-4471-87d5-b565b9aaef77',
        '2022/04':'https://datacenter.taichung.gov.tw/swagger/OpenData/d50b89d8-f250-46d2-963f-5bc42bc80ba2',
        '2022/03':'https://datacenter.taichung.gov.tw/swagger/OpenData/f4915371-c407-412e-9cda-27b15462aa57',
        '2022/02':'https://datacenter.taichung.gov.tw/swagger/OpenData/e4b34148-97dd-4a55-8bfc-b8c2eea49b25',
        '2022/01':'https://datacenter.taichung.gov.tw/swagger/OpenData/99a12c91-0a14-474d-b1a2-79c84b8b0cee'
    }
    header={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    taichung_traffic_volume=[]

    for year_month in taichung_data_url_list:
        data = json.loads(requests.get(taichung_data_url_list.get(year_month)).text)
        total = 0
        for day_data in data:
            total += int(day_data.get("總運量").replace(',',''))
        taichung_traffic_volume.append(total)
        # print(year_month ,'總運量:', total)
    print(taichung_traffic_volume)


#台北#######################################################################################################################
    response = requests.get('https://data.gov.tw/dataset/128641')
    p = BeautifulSoup(response.text, 'lxml').select("div.download-item a")
    temp=''
    taipei_traffic_volume=[]
    for i in range(len(p)-10,len(p)):
        total=0
        temp = p[i]['href']
        result = requests.get(temp).text
        cr = csv.reader(result, dialect=csv.excel_tab)
        for row in cr:
            try:
                if(len(row[0])>6):
                    total+=int(row[0].replace(',',''))
            except:
                pass
        taipei_traffic_volume.append(total)
    print(taipei_traffic_volume)
#台北送醫
    response = requests.get('https://data.gov.tw/dataset/121979')
    p = BeautifulSoup(response.text, 'lxml').select("div.download-item a")
    temp=''
    taipei_epi=[]
    for i in range(len(p)-10,len(p)):
        total=0
        temp = p[i]['href']
        result = requests.get(temp).content
        with open('temp.csv','wb') as csvv:
            csvv.write(result)
        with open('temp.csv') as csvv:
            cr = csv.reader(csvv, dialect=csv.excel_tab,delimiter=',')
            for row in cr:
                if row[0]=='總計 ':
                    taipei_epi.append(int(row[8]))
    print(taipei_epi)
    plt.plot(time, taipei_epi, color=(55/255,100/255,10/255))
    plt.show()

#確診#######################################################################################################################
    url = "https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4051&limited=TWN"
    response = requests.get(url)
    data = json.loads(response.text)
    month = '01'
    total = 0
    plot_numlist=[]
    for i in data:
        if month=='11':
            break
        data_month = i.get('a04').split('-')[1]
        data_num = i.get('a06')
        if month==data_month:
            total += int(data_num)
        else:
            # print(month , numsum)
            plot_numlist.append(total)
            month = data_month
            total = 0
    print(plot_numlist)
    

# #繪圖#######################################################################################################################
    fig, axs = plt.subplots(3)

    axs[0].plot(time, taipei_traffic_volume, color=(255/255,100/255,100/255))
    axs[0].set_title(u'Traffic volume of Taipei MRT')

    axs[1].plot(time, taichung_traffic_volume, color=(255/255,100/255,100/255))
    axs[1].set_title(u'Traffic volume of Taichung MRT')

    axs[2].plot(time, plot_numlist, color=(55/255,100/255,10/255))
    axs[2].set_title(u'Number of confirmed cases')

    plt.show()
