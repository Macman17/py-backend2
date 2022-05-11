

from bson import ObjectId
from flask import Flask, request, abort
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
    prod = db.products.find_one({"_id": ObjectId(id)})

    prod["_id"] = str(prod["_id"]) 

    return json.dumps(prod)


@app.route("/api/products/category")
def get_catagories():
    cursor= db.products.find({})
    catagories = []  
    

    for prod in cursor:
        cat = prod["category"]
        if not cat in catagories:
            catagories.append(cat)

    catagories["_id"] = str(catagories["_id"]) 
    return json.dumps(catagories)

@app.route("/api/products/category/<cat_name>")

def get_title(cat_name):
    cursor= db.products.find({"category": cat_name})
    results = []

    for prod in cursor:
        if prod["category"].lower() == cat_name.lower() :
            results.append(prod)
    prod["_id"] = str(prod["_id"]) 
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

@app.get("/api/couponCodes")
def get_coupon():

    cursor= db.couponCodes.find({})
    results= []

    for code in cursor:
        code["_id"] = str(code["_id"]) 
        results.append(code)
        
    return json.dumps(results)

@app.get("/api/couponCodes/<code>")
def get_by_code_coupon(code):

    coupon = db.couponCodes.find_one({"code": code})
    if not coupon:
        return abort(400, "Invalid coupon code")

    
    code["_id"] = str(code["_id"]) 
    return json.dumps(coupon)


@app.route("/api/couponCodes", methods=["post"])
def save_coupon():
    coupon = request.get_json()

    if not "code" in coupon or len(coupon["code"]) < 5:
        return abort(400, "Code is required and should contains at least 5 chars.")

    if not "discount" in coupon or type(coupon["discount"]) != type(int) or type(coupon["discount"]) != type(float):
        return abort(400, "Discount is required and should a valid number.")

    if coupon < 0 or len(coupon["discount"]) > 31:
        return abort(400, "Discount should be lower than 31.")

    db.couponCode.insert_one(coupon)
    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)


app.run(debug=True)
