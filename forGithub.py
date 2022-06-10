import requests
url = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=2021'
url += '0101&end=20211230&valcode=eur&sort=exchangedate&order=desc&json'
myfile = requests.get(url)
open('data2.json', 'wb').write(myfile.content)
import json
import csv
with open('data2.json', encoding='utf-8') as json_file:
    exchange_rates = json.load(json_file)
data_file = open('data_file2.csv', 'w')
csv_writer = csv.writer(data_file)
count = 0
for rate in exchange_rates:
    if count == 0:
        header = rate.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(rate.values())
data_file.close()



import boto3
import os
import configparser
import pandas as pd
import numpy
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
config = configparser.RawConfigParser()
path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
config.read(path)
ACCESS_KEY = config.get('default', 'aws_access_key_id')
SECRET_KEY = config.get('default','aws_secret_access_key')
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)
s3.download_file('labbucket0', 'data_file.csv', 'temp_data_file.csv')


df = pd.read_csv('temp_data_file.csv')
df = df[::-1]
x = df['calcdate']
y = df['rate_per_unit']
df1 = pd.read_csv('data_file2.csv')
df1 = df1[::-1]
z = df1['rate_per_unit']
fig, ax = plt.subplots()
x_ticks = numpy.arange(0, len(df), len(df)/5)
ax.set_xticks(x_ticks)
plt.plot(x, y, label='USD')
plt.ylabel("exchange rate of UAH")
plt.plot(x, z, label='EUR')


newDF = pd.DataFrame({'date': x, 'USD':y, 'EUR': z})
newDF.to_csv('mainData.csv', index = False)

with open("mainData.csv", "rb") as f:
    s3.upload_fileobj(f, 'labbucket0', "mainData.csv")

plt.savefig('exchange_rates.png')
plt.legend()
os.remove('data2.json')
os.remove('data_file2.csv')
os.remove('temp_data_file.csv')
#plt.savefig('exchange_rates.png')
with open("exchange_rates.png", "rb") as f:
    s3.upload_fileobj(f, 'labbucket0', "exchange_rates.png")

os.remove('exchange_rates.png')
