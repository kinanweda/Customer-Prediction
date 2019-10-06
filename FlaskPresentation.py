from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import matplotlib as plt
import plotly.graph_objects as go
import requests,plotly,json,folium

app = Flask(__name__)

df = pd.read_csv("data.csv", encoding="ISO-8859-1", dtype={'CustomerID': str,'InvoiceID': str})
df.replace({'':np.NaN},inplace=True)
cache={'foo':0,'page':'data'}

dfCleaned = pd.read_csv('dfCleaned.csv', index_col = False)
dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')

def create_plot():
    dfCleaned = pd.read_csv('dfCleaned.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    listSpecialCode = dfCleaned[dfCleaned['StockCode'].str.contains('^[a-zA-Z]+', regex=True)]['StockCode'].unique()
    for i in listSpecialCode:
        dfCleaned = dfCleaned.drop(dfCleaned[dfCleaned['StockCode']==i].index,axis=0)
    dfCleaned['TotalPrice'] = dfCleaned['UnitPrice'] * (dfCleaned['Quantity'] - dfCleaned['QuantityCanceled'])
    dfCleaned['InvoiceDate'] = pd.to_datetime(dfCleaned['InvoiceDate'])

    temp = dfCleaned.groupby(by=['CustomerID', 'InvoiceNo'], as_index=False)['TotalPrice'].sum()
    basketPrice = temp.rename(columns = {'TotalPrice':'Basket Price'})
    #_____________________
    # Tanggal pemesanan
    dfCleaned['InvoiceDate_int'] = dfCleaned['InvoiceDate'].astype('int64')
    temp = dfCleaned.groupby(by=['CustomerID', 'InvoiceNo'], as_index=False)['InvoiceDate_int'].mean()
    dfCleaned.drop('InvoiceDate_int', axis = 1, inplace = True)
    basketPrice.loc[:, 'InvoiceDate'] = pd.to_datetime(temp['InvoiceDate_int'])
    basketPrice = basketPrice[basketPrice['Basket Price'] > 0]
    basketPrice.sort_values('CustomerID')


    prices = [0, 50, 100, 200, 500, 1000, 5000, 50000]
    labels = ['Total Basket Price Range: 0','Total Basket Price Range: 50','Total Basket Price Range: 100','Total Basket Price Range: 200','Total Basket Price Range: 500','Total Basket Price Range: 1000','Total Basket Price Range: 5000','Total Basket Price Range: 50000',]
    values = []
    for i, price in enumerate(prices):
        if i == 0: continue
        val = basketPrice[(basketPrice['Basket Price'] < price) &
                        (basketPrice['Basket Price'] > prices[i-1])]['Basket Price'].count()
        values.append(val)

    data=[go.Pie(labels=labels, values=values)]
    graphJson = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJson

@app.route('/', methods=['POST','GET'])
def home():
    requestForm = request.form.to_dict()
    header = df.columns.tolist()
    length = df.iloc[0:100].index
    bar = create_plot()
    if request.method == 'POST' :
        if requestForm['submit_button'] == 'Next': 
            cache['foo'] += 1
            length = df.iloc[(cache['foo']*100):((cache['foo']*100)+100)].index
        elif requestForm['submit_button'] == 'Previous':
            if cache['foo'] == 0:
                cache['foo'] = 0
                length = df.iloc[(cache['foo']*100):((cache['foo']*100)+100)].index
            else:
                cache['foo'] -= 1
                length = df.iloc[(cache['foo']*100):((cache['foo']*100)+100)].index   
        elif requestForm['submit_button'] in list(df['CustomerID']):
            length = df[df['CustomerID'] == requestForm['submit_button']].index
    return render_template('index.html', headers=header, length=length, df=df, page=cache['page'], plot = bar )


if (__name__) == '__main__':
    app.run(
        debug=True,
        host='localhost',
        port=5000
        )