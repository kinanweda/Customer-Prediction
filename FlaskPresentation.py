from flask import Flask, render_template, request, redirect
from datetime import date, timedelta
import numpy as np
import pandas as pd
import matplotlib as plt
import plotly.graph_objects as go
import requests,plotly,json,folium,mysql.connector, sqlalchemy, pickle, sqlalchemy,datetime


app = Flask(__name__)

db = mysql.connector.connect(
    host =  '127.0.0.1',
    port = 3306,
    user = 'kinanweda',
    passwd = 'Jimbamamba22',
    database = 'ProjectAkhir' 
)


conn = sqlalchemy.create_engine(
    'mysql+pymysql://kinanweda:Jimbamamba22@localhost:3306/ProjectAkhir'
)

country_geo = 'world-countries.json'

df = pd.read_csv("data.csv", encoding="ISO-8859-1", dtype={'CustomerID': str,'InvoiceID': str})
df.replace({'':np.NaN},inplace=True)
cache={'foo':0,'page':'data'}

dfCleaned = pd.read_csv('dfCleaned.csv', index_col = False)
dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')

def loadEncoder():
    global labelEncoder
    with open('labelencoder.pickle','rb') as j:
        labelEncoder = pickle.load(j)

def loadCluster():
    global clusters
    with open('product_clusters.pickle','rb') as x :
        clusters = pickle.load(x)

def loadModel():
    global model
    with open('modelpredict.pkl','rb') as y :
        model = pickle.load(y)

def loadScaler():
    global scaler
    with open('scaler.pickle','rb') as f :
        scaler = pickle.load(f)


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

    data=[go.Pie(labels=labels, values=values, title='Transactions Distirbution', titleposition='top center', titlefont=dict(size=25))]
    graphJson = json.dumps(data,cls=plotly.utils.PlotlyJSONEncoder)
    # print(graphJson)
    return graphJson


def bar_plot():
    body = request.form
    dfCleaned = pd.read_csv('dfCleaned_2.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    dfFinal = pd.read_csv('final_dataset_V2.csv')
    cust0 = list(dfFinal[dfFinal['cluster']==0]['CustomerID'])
    cluster0 = dfCleaned[dfCleaned['CustomerID'].isin(cust0)]
    x = sorted(cluster0['Month'].unique())
    y = cluster0['Month'].value_counts().sort_index()
    data = [go.Bar(
            x=x,
            y=y,
        )
    ]

    barGraph = json.dumps(data,cls=plotly.utils.PlotlyJSONEncoder)
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

@app.route('/')
def home():
    return render_template('reg.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
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
    dfPredict = pd.read_sql('datacust', conn)
    dfPredict['TotalPrice'] = dfPredict['UnitPrice'] * (dfPredict['Quantity'] - dfPredict['QuantityCanceled'])
    dfPredict['InvoiceDate'] = pd.to_datetime(dfPredict['InvoiceDate'])
    dfPredict['Country'] = labelEncoder.transform(dfPredict['Country'])
    today = date.today() + timedelta(days=1)
    now = datetime.datetime(today.year,today.month,today.day)
    dfPredict['InvoiceDate'] = pd.to_datetime(dfPredict['InvoiceDate'])
    customAggregation = {}
    customAggregation["InvoiceDate"] = lambda x:x.iloc[0]
    customAggregation["CustomerID"] = lambda x:x.iloc[0]
    customAggregation["TotalPrice"] = "sum"
    rfmTable = dfPredict.groupby("InvoiceNo").agg(customAggregation)
    rfmTable["Recency"] = now - rfmTable["InvoiceDate"]
    rfmTable["Recency"] = pd.to_timedelta(rfmTable["Recency"]).astype("timedelta64[D]")
    customAggregation = {}
    customAggregation["Recency"] = ["min", "max"]
    customAggregation["InvoiceDate"] = lambda x: len(x)
    customAggregation["TotalPrice"] = "sum"
    rfmTableFinal = rfmTable.groupby("CustomerID").agg(customAggregation)
    rfmTableFinal.columns = ["min_recency", "max_recency", "frequency", "monetary_value"]
    quantiles = rfmTableFinal.quantile(q=[0.25,0.5,0.75])
    quantiles = quantiles.to_dict()
    segmentedRFM = rfmTableFinal

    def RScore(x,p,d):
        if x <= d[p][0.25]:
            return 1
        elif x <= d[p][0.50]:
            return 2
        elif x <= d[p][0.75]: 
            return 3
        else:
            return 4
        
    def FMScore(x,p,d):
        if x <= d[p][0.25]:
            return 4
        elif x <= d[p][0.50]:
            return 3
        elif x <= d[p][0.75]: 
            return 2
        else:
            return 1

    segmentedRFM['r_quartile'] = segmentedRFM['min_recency'].apply(RScore, args=('min_recency',quantiles,))
    segmentedRFM['f_quartile'] = segmentedRFM['frequency'].apply(FMScore, args=('frequency',quantiles,))
    segmentedRFM['m_quartile'] = segmentedRFM['monetary_value'].apply(FMScore, args=('monetary_value',quantiles,))
    segmentedRFM['RFMScore'] = segmentedRFM['r_quartile'].astype('str')+segmentedRFM['f_quartile'].astype('str')+segmentedRFM['m_quartile'].astype('str')
    dfPredict = pd.merge(dfPredict,segmentedRFM, on='CustomerID')
    dfPredict = dfPredict.drop(columns=['r_quartile', 'f_quartile', 'm_quartile'])
    dfPredict['Month'] = dfPredict["InvoiceDate"].map(lambda x: x.month)
    dfPredict['Weekday'] = dfPredict["InvoiceDate"].map(lambda x: x.weekday())
    dfPredict['Day'] = dfPredict["InvoiceDate"].map(lambda x: x.day)
    dfPredict['Hour'] = dfPredict["InvoiceDate"].map(lambda x: x.hour)
    cluster = dfPredict['Description'].apply(lambda x : clusters[x])
    df2 = pd.get_dummies(cluster, prefix="Cluster").mul(dfPredict["TotalPrice"], 0)
    df2 = pd.concat([dfPredict['InvoiceNo'], df2], axis=1)
    df2_grouped = df2.groupby('InvoiceNo').sum()
    customAggregation = {}
    customAggregation["TotalPrice"] = lambda x:x.iloc[0]
    customAggregation["min_recency"] = lambda x:x.iloc[0]
    customAggregation["max_recency"] = lambda x:x.iloc[0]
    customAggregation["frequency"] = lambda x:x.iloc[0]
    customAggregation["monetary_value"] = lambda x:x.iloc[0]
    customAggregation["CustomerID"] = lambda x:x.iloc[0]
    customAggregation["Quantity"] = "sum"
    customAggregation["Country"] = lambda x:x.iloc[0]
    df_grouped = dfPredict.groupby("InvoiceNo").agg(customAggregation)
    customAggregation = {}
    customAggregation["TotalPrice"] = ['min','max','mean']
    customAggregation["min_recency"] = lambda x:x.iloc[0]
    customAggregation["max_recency"] = lambda x:x.iloc[0]
    customAggregation["frequency"] = lambda x:x.iloc[0]
    customAggregation["monetary_value"] = lambda x:x.iloc[0]
    customAggregation["Quantity"] = "sum"
    customAggregation["Country"] = lambda x:x.iloc[0]
    df_grouped_final = df_grouped.groupby("CustomerID").agg(customAggregation)
    df_grouped_final.columns = ["min", "max", "mean", "min_recency", "max_recency", "frequency", "monetary_value", "quantity", "country"]
    df2_grouped_final = pd.concat([df_grouped['CustomerID'], df2_grouped], axis=1).set_index("CustomerID").groupby("CustomerID").sum()
    df2_grouped_final = df2_grouped_final.div(df2_grouped_final.sum(axis=1), axis=0)
    df2_grouped_final = df2_grouped_final.fillna(0)
    df3 = df2_grouped_final.copy()
    for j in df3.columns:
        df3.drop(str(j),axis=1,inplace=True)
    for i in range(135):
        df3['Cluster_' + str(i)] = 0.0
    df2_grouped_final = df2_grouped_final.reindex(sorted(df2_grouped_final.columns), axis=1)
    for i in df2_grouped_final.columns.values:
        df3[i] = df3[i].replace({0.0:df2_grouped_final[i].values.tolist()})
    X1 = df_grouped_final.as_matrix()
    X2 = df3.as_matrix()
    X1 = scaler.transform(X1)
    X_final_std_scale = np.concatenate((X1, X2), axis=1)
    hasilCLuster = model.predict(X_final_std_scale)
    df_grouped_final["cluster"] = hasilCLuster
    df_grouped_final = df_grouped_final.reset_index()
    head = df_grouped_final.columns.tolist()
    lengths = df_grouped_final.index
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
                body=request.form
                print(body['submit_button'])
        # elif requestForm['submit_button'] in list(df['Country']):
        #         length = df[df['Country'] == requestForm['submit_button']].index
        elif requestForm['submit_button'] == 'Fullscreen':
            return redirect('/map')
        
    return render_template('index.html', dfPrediksi = df_grouped_final, head = head, lengths = lengths, headers=header, length=length, df=df, page=cache['page'], plot = pie, plotbar= bar , plotbar1=bar1, plotbar2=bar2,plotbar3=bar3,plotbar4=bar4,plotbar5=bar5,plotbar6=bar6,plotbar7=bar7)

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

@app.route('/creator', methods=['POST','GET'])
def creator():
    dfCleaned = pd.read_csv('dfCleaned.csv', index_col = False)
    dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
    produk = dfCleaned['Description'].unique()
    country = dfCleaned['Country'].unique()
    if request.method == 'POST':
        dfCleaned = pd.read_csv('dfCleaned.csv', index_col = False)
        dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
        body = request.form
        used = db.cursor()
        deskripsi = body['description']
        harga = round(dfCleaned[dfCleaned['Description'] == body['description']]['UnitPrice'].mean(),2)
        quantitas = body['quantity']
        a = {key:val for key,val in zip(dfCleaned['Description'].values.tolist(),dfCleaned['StockCode'].values.tolist())}
        stock = a[body['description']]
        customer = body['customer']
        negara = body['country']
        email = body['email']
        qry1 = 'select * from login where email = %s'
        val1 = (email,)
        used.execute(qry1,val1)
        hasil = used.fetchall()
        cust = hasil[0][0]
        password = body['password']
        qry = 'insert into datacust (StockCode,Description,Quantity,UnitPrice,CustomerID,Country) values(%s,%s,%s,%s,%s,%s)'
        val = (stock,deskripsi,quantitas,harga,customer,negara)
        used.execute(qry, val)
        db.commit()
        return render_template('success.html', email=email, password=password, cust=cust) #cost=cost)
    return render_template('creator.html',produk=produk, country=country)

@app.route('/signup', methods = ['POST'])
def signup():
    try:
        request.method == 'POST'
        # body = request.json
        body = request.form
        used = db.cursor()
        qry = 'insert into login (email, password) values(%s,%s)'
        val = (body['email'],body['password'])
        used.execute(qry, val)
        db.commit()
        return redirect('/')    
    except mysql.connector.Error:
        msg = 'Customer ID has been registered!'
        return render_template('reg.html', msg1=msg) 

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        body = request.form
        email = body['email']
        password = body['password']
        used = db.cursor()
        qry = 'select * from login where email = %s'
        val = (email,)
        used.execute(qry,val)
        hasil = used.fetchall()
        msg = 'Your Email Has Not Been Registered!'
        if hasil == []:
            return render_template('reg.html', msg2=msg)
        else:
            qry = 'select * from login where email = %s and password = %s'
            val = (body['email'],body['password'])
            used.execute(qry,val)
            hasil = used.fetchall()
            msg = 'Your password is wrong!'
            if hasil == [] :
                return render_template('reg.html', msg3= msg)
            else :
                cust = hasil[0][0]
                dfCleaned = pd.read_csv('dfCleaned.csv', index_col = False)
                dfCleaned = dfCleaned.drop('Unnamed: 0',axis='columns')
                produk = dfCleaned['Description'].unique()
                country = dfCleaned['Country'].unique()
                return render_template('creator.html', cust=cust, produk=produk, country=country, email=email,password=password)

if (__name__) == '__main__':
    loadCluster()
    loadEncoder()
    loadModel()
    loadScaler()
    app.run(
        debug=True,
        host='localhost',
        port=5000
        )