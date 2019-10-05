from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import matplotlib as plt
import requests

app = Flask(__name__)

df = pd.read_csv("data.csv", encoding="ISO-8859-1", dtype={'CustomerID': str,'InvoiceID': str})
df.replace({'':np.NaN},inplace=True)
cache={'foo':0,'page':'data'}
@app.route('/', methods=['POST','GET'])
def home():
    requestForm = request.form.to_dict()
    header = df.columns.tolist()
    length = df.iloc[0:100].index
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
    return render_template('index.html', headers=header, length=length, df=df, page=cache['page'] )


if (__name__) == '__main__':
    app.run(
        debug=True,
        host='localhost',
        port=5000
        )