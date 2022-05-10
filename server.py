
from flask import Flask, request
import json
from mock_data import mock_catalog
from config import db

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
    cursor = db.products.find({}) #get all
    all_products = []

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        all_products.append(prod)

    return json.dumps(all_products)    


@app.route("/api/catalog", methods=["post"])
def save_product():
    product = request.get_json()
    db.products.insert_one(product)

    print("Product saved!")
    print(product)

    #fix the id issue
    product["_id"] = str(product["_id"])

    return json.dumps(product) # crash



@app.route("/api/catalog/cheapest")
def get_cheapest():    
    print("cheapest product")

    db_prod= db.products.find({})
    solution= db_prod[0]
    for prod in db_prod:
        if prod["unitPrice"] < solution["unitPrice"]:
            solution = prod


    solution["_id"] = str(solution["_id"])       
    return json.dumps(solution)

@app.route("/api/catalog/total")
def get_total(): 
    print("total")

    db_prod= db.products.find({})
    total = 0
    for prod in db_prod:
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
