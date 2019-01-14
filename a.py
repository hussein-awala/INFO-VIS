import pandas as pd
import numpy as np
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/get_json')
def get_json():
    country=request.args['country']
    url='google'
    countries=pd.read_csv('tsv/products_countries.tsv','\t')
    products=pd.read_csv('tsv/products.tsv','\t',low_memory=False)[['code','name']]
    additives=pd.read_csv('tsv/products_additives.tsv','\t')
    d=pd.merge(countries[countries['country']==country],pd.merge(products,additives,how='inner',left_on='code',right_on='code'),how='inner',left_on='code',right_on='code')[['code','name','additive']][:20000]
    data=[]
    groups=d.groupby('additive')
    for name,g in groups:
        additive=dict({})
        additive['name']=name
        additive['count']=g.shape[0]
        additive['key']=name
        pages=[]
        for i,p in g.iterrows():
            product=dict({})
            product['name']=p['name']
            product['key']=p['code']
            product['title']=p['name']
            product['url']=url+p['code']
            pages.append(product)
        additive['pages']=pages
        data.append(additive)
    return jsonify(data)
@app.route('/get_products_info')
def get_products_info():
    country=request.args['country']
    countries=pd.read_csv('tsv/products_countries.tsv','\t',low_memory=False)
    products_in_country=pd.DataFrame(countries[countries['country']==country]['code'])
    product=pd.read_csv('tsv/products.tsv','\t',low_memory=False)[['code','energy_100g','n_additives','proteins_100g','fat_100g','carbohydrates_100g','sugars_100g','saturated-fat_100g','salt_100g','sodium_100g']]
    product=products_in_country.merge(product,left_on='code',right_on='code')
    data=dict({})
    means=product.mean()
    stds=product.std()
    for i in product.columns:
        if(i=='code'):
            continue
        l=np.array(product[i].dropna().tolist())
        data[i]=l[np.logical_and(l>means[i]-2*stds[i],(l<means[i]+2*stds[i]))].tolist()
    return jsonify(data)
if __name__ == "__main__":
	app.run()

