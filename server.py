

from turtle import title
from unicodedata import category
from unittest import result
from flask import Flask
import json
from mock_data import mock_catalog

app = Flask('server')


@app.route("/")
def root():
    return "Welcome to the root page"


@app.route("/api/about")
def about():
    me = {
        "first": "Naqui",
        "last": "Darby"
    }
    return json.dumps(me)  # parse into json, then return


@app.route("/api/catalog")
def get_catalog():
    return json.dumps(mock_catalog)

@app.route("/api/catalog/cheapest")
def get_cheapest():    
    print("cheapest product")

    cheap_prod= mock_catalog[0]
    for prod in mock_catalog:
        if prod["unitPrice"] < cheap_prod["unitPrice"]:
            cheap_prod = prod

        
    return json.dumps(cheap_prod)

@app.route("/api/catalog/total")
def get_total(): 
    print("total")

    total = 0
    for prod in mock_catalog:
        total += prod["unitPrice"]

    return json.dumps(total) 

@app.route("/api/products/<id>")
def find_product(id):
    for prod in mock_catalog:
        if id == prod["_id"]:
            return json.dumps(prod) 


@app.route("/api/products/category")
def get_catagories():
    catagories = []

    for prod in mock_catalog:
        cat = prod["category"]
        if not cat in catagories:
            catagories.append(cat)

    return json.dumps(catagories)

@app.route("/api/products/category/<cat_name>")

def get_title(cat_name):
    results = []

    for prod in mock_catalog:
        if prod["category"].lower() == cat_name.lower() :
            results.append(prod)

    return json.dumps(results)    

@app.route("/api/products/search/<text>")
def search_by_text(text):
    results = []
    text = text.lower()
    # search and add
    for prod in mock_catalog:
        title = prod["title"].lower()
        if  text in title:
            results.append(prod)        

    return json.dumps(results)



app.run(debug=True)
