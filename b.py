import pandas as pd
import numpy as np
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/get_products_info')
def get_products_info():
    country=request.args['country']
    countries=pd.read_csv('tsv/products_countries.tsv','\t',low_memory=False)
    products_in_country=pd.DataFrame(countries[countries['country']==country]['code'])
    product=pd.read_csv('tsv/products.tsv','\t',low_memory=False)[['code','energy_100g','n_additives','proteins_100g','fat_100g','carbohydrates_100g','sugars_100g','saturated-fat_100g','salt_100g','sodium_100g']]
    product=products_in_country.merge(x,left_on='code',right_on='code')
    print(product)
if __name__ == "__main__":
	app.run()

