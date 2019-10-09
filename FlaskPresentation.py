from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
import matplotlib as plt
import plotly.graph_objects as go
import requests,plotly,json,folium

app = Flask(__name__)

country_geo = 'world-countries.json'

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

# def bar_plot():
#     body = request.form
#     dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
#     dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
#     dfFinal = pd.read_csv('final_dataset_V2.csv')
#     cust0 = list(dfFinal[dfFinal['cluster']==0]['CustomerID'])
#     cluster0 = dfCleaned[dfCleaned['CustomerID'].isin(cust0)]
#     cust1 = list(dfFinal[dfFinal['cluster']==1]['CustomerID'])
#     cluster1 = dfCleaned[dfCleaned['CustomerID'].isin(cust1)]
#     cust2 = list(dfFinal[dfFinal['cluster']==2]['CustomerID'])
#     cluster2 = dfCleaned[dfCleaned['CustomerID'].isin(cust2)]
#     cust3 = list(dfFinal[dfFinal['cluster']==3]['CustomerID'])
#     cluster3 = dfCleaned[dfCleaned['CustomerID'].isin(cust3)]
#     cust4 = list(dfFinal[dfFinal['cluster']==4]['CustomerID'])
#     cluster4 = dfCleaned[dfCleaned['CustomerID'].isin(cust4)]
#     cust5 = list(dfFinal[dfFinal['cluster']==5]['CustomerID'])
#     cluster5 = dfCleaned[dfCleaned['CustomerID'].isin(cust5)]
#     cust6 = list(dfFinal[dfFinal['cluster']==6]['CustomerID'])
#     cluster6 = dfCleaned[dfCleaned['CustomerID'].isin(cust6)]
#     cust7 = list(dfFinal[dfFinal['cluster']==7]['CustomerID'])
#     cluster7 = dfCleaned[dfCleaned['CustomerID'].isin(cust7)]
#     x = sorted(cluster0['Month'].unique())
#     y = cluster0['Month'].value_counts().sort_index()
#     x1 = sorted(cluster0['Month'].unique())
#     y1 = cluster0['Month'].value_counts().sort_index()
#     x2 = sorted(cluster0['Month'].unique())
#     y2 = cluster0['Month'].value_counts().sort_index()
#     x3 = sorted(cluster0['Month'].unique())
#     y3 = cluster0['Month'].value_counts().sort_index()
#     x4 = sorted(cluster0['Month'].unique())
#     y4 = cluster0['Month'].value_counts().sort_index()
#     x5 = sorted(cluster0['Month'].unique())
#     y5 = cluster0['Month'].value_counts().sort_index()
#     x6 = sorted(cluster0['Month'].unique())
#     y6 = cluster0['Month'].value_counts().sort_index()
#     x7 = sorted(cluster0['Month'].unique())
#     y7 = cluster0['Month'].value_counts().sort_index()
#     fig = go.Figure()

#     # Add traces
#     fig.add_trace(
#         data = [go.Bar(
#                 x=x,
#                 y=y
#             )]
#     )

#     fig.add_trace(
#         data = [go.Bar(
#                 x=x1,
#                 y=y1
#             )]
#     )

#     fig.add_trace(
#         data = [go.Bar(
#                 x=x2,
#                 y=y2
#             )]
#     )

#     fig.add_trace(
#         data = [go.Bar(
#                 x=x3,
#                 y=y3
#             )]
#     )
    
#     fig.add_trace(
#         data = [go.Bar(
#                 x=x4,
#                 y=y4
#             )]
#     )

#     fig.add_trace(
#         data = [go.Bar(
#                 x=x5,
#                 y=y5
#             )]
#     )

#     fig.add_trace(
#         data = [go.Bar(
#                 x=x6,
#                 y=y6
#             )]
#     )

#     fig.add_trace(
#         data = [go.Bar(
#                 x=x7,
#                 y=y7
#             )]
#     )

#     fig.update_layout(
#         updatemenus=[
#             go.layout.Updatemenu(buttons=list([
#                 dict(label="Cluster 0",
#                     method="relayout",
#                     args=["shapes", cluster0]),
#                 dict(label="Cluster 1",
#                     method="relayout",
#                     args=["shapes", cluster1]),
#                 dict(label="Cluster 2",
#                     method="relayout",
#                     args=["shapes", cluster2]),
#                 dict(label="Cluster 3",
#                     method="relayout",
#                     args=["shapes", cluster3]),
#                 dict(label="Cluster 0",
#                     method="relayout",
#                     args=["shapes", cluster4]),
#                 dict(label="Cluster 1",
#                     method="relayout",
#                     args=["shapes", cluster5]),
#                 dict(label="Cluster 2",
#                     method="relayout",
#                     args=["shapes", cluster6]),
#                 dict(label="Cluster 3",
#                     method="relayout",
#                     args=["shapes", cluster7]),
#             ]),
#             )
#         ]
#     )

#     # Update remaining layout properties
#     fig.update_layout(
#         title_text="Highlight Clusters",
#         showlegend=False,
#     )
#     chart_link = api_create(p, filename="dropdown-2")
#     chart_link


def bar_plot():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust0 = list(dfFinal[dfFinal['cluster']==0]['CustomerID'])
    cluster0 = dfCleaned[dfCleaned['CustomerID'].isin(cust0)]
    x = sorted(cluster0['Month'].unique())
    y = cluster0['Month'].value_counts().sort_index()
    data = [
        go.Bar(
            x=x,
            y=y
        )
    ]

    barGraph = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph

def bar_plot1():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust1 = list(dfFinal[dfFinal['cluster']==1]['CustomerID'])
    cluster1 = dfCleaned[dfCleaned['CustomerID'].isin(cust1)]
    x = sorted(cluster1['Month'].unique())
    y = cluster1['Month'].value_counts().sort_index()
    data = [
        go.Bar(
            x=x,
            y=y
        )
    ]

    barGraph1 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph1

def bar_plot2():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust2 = list(dfFinal[dfFinal['cluster']==2]['CustomerID'])
    cluster2 = dfCleaned[dfCleaned['CustomerID'].isin(cust2)]
    x = sorted(cluster2['Month'].unique())
    y = cluster2['Month'].value_counts().sort_index()
    data = [
        go.Bar(
            x=x,
            y=y
        )
    ]

    barGraph2 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph2

def bar_plot3():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust3 = list(dfFinal[dfFinal['cluster']==3]['CustomerID'])
    cluster3 = dfCleaned[dfCleaned['CustomerID'].isin(cust3)]
    x = sorted(cluster3['Month'].unique())
    y = cluster3['Month'].value_counts().sort_index()
    data = [
        go.Bar(
            x=x,
            y=y
        )
    ]

    barGraph3 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph3

def bar_plot4():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust4 = list(dfFinal[dfFinal['cluster']==4]['CustomerID'])
    cluster4 = dfCleaned[dfCleaned['CustomerID'].isin(cust4)]
    x = sorted(cluster4['Month'].unique())
    y = cluster4['Month'].value_counts().sort_index()
    data = [
        go.Bar(
            x=x,
            y=y
        )
    ]

    barGraph4 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph4

def bar_plot5():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust5 = list(dfFinal[dfFinal['cluster']==5]['CustomerID'])
    cluster5 = dfCleaned[dfCleaned['CustomerID'].isin(cust5)]
    x = sorted(cluster5['Month'].unique())
    y = cluster5['Month'].value_counts().sort_index()
    data = [
        go.Bar(
            x=x,
            y=y
        )
    ]

    barGraph5 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph5

def bar_plot6():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust6 = list(dfFinal[dfFinal['cluster']==6]['CustomerID'])
    cluster6 = dfCleaned[dfCleaned['CustomerID'].isin(cust6)]
    x = sorted(cluster6['Month'].unique())
    y = cluster6['Month'].value_counts().sort_index()
    data = [
        go.Bar(
            x=x,
            y=y
        )
    ]

    barGraph6 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph6

def bar_plot7():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust7 = list(dfFinal[dfFinal['cluster']==7]['CustomerID'])
    cluster7 = dfCleaned[dfCleaned['CustomerID'].isin(cust7)]
    x = sorted(cluster7['Month'].unique())
    y = cluster7['Month'].value_counts().sort_index()
    data = [
        go.Bar(
            x=x,
            y=y
        )
    ]

    barGraph7 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph7

@app.route('/', methods=['POST','GET'])
def home():
    requestForm = request.form.to_dict()
    header = df.columns.tolist()
    length = df.iloc[0:100].index
    pie = create_plot()
    bar = bar_plot()
    bar1 = bar_plot1()
    bar2 = bar_plot2()
    bar3 = bar_plot3()
    bar4 = bar_plot4()
    bar5 = bar_plot5()
    bar6 = bar_plot6()
    bar7 = bar_plot7()
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
        # elif requestForm['submit_button'] in list(df['Country']):
        #         length = df[df['Country'] == requestForm['submit_button']].index
        elif requestForm['submit_button'] == 'Fullscreen':
            return redirect('/map')
    return render_template('index.html', headers=header, length=length, df=df, page=cache['page'], plot = pie, plotbar= bar , plotbar1=bar1, plotbar2=bar2,plotbar3=bar3,plotbar4=bar4,plotbar5=bar5,plotbar6=bar6,plotbar7=bar7)

@app.route('/map')
def foliumMap():
    idCountry = pd.read_json('world-countries.json')
    idCountry['features']
    a = [i['id'] for i in idCountry['features']]
    b = [j['properties']['name'] for j in idCountry['features']]

    listIdCountry = pd.DataFrame({
        'Negara':b,
        'id' : a,
    })
    a = 0
    listTotal = []
    listCountry = []
    listPct = []
    for i,item in enumerate(df['Country'].unique()):
        listTotal.append(df[(df['Country']== item ) & True].shape[0])
        a = a + df[(df['Country']== item ) & True].shape[0]
        listCountry.append(item)
        listPct.append(round((listTotal[i]/df.shape[0])*100,2))

    country = pd.DataFrame({'Negara' : df['Country'].unique(),'Total Customer' : listTotal,'Percentage' : listPct})
    country = pd.merge(country,listIdCountry,left_on ='Negara', right_on ='Negara',how='left')
    map = folium.Map(
        location=[53.2202105,-22.2277193], zoom_start=4
    )

    map.choropleth(geo_data=country_geo, data=country,
             columns=['id', 'Percentage'],
             key_on='feature.id',
             fill_color='YlGnBu', fill_opacity=0.8, line_opacity=0.2,
             legend_name='Total Customer')
    map.save('templates/map.html')
    return render_template('map.html')


if (__name__) == '__main__':
    app.run(
        debug=True,
        host='localhost',
        port=5000
        )