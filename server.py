

from itertools import product
from bson import ObjectId
from flask import Flask, request, abort
import json
from mock_data import mock_catalog
from config import db
from flask_cors import CORS

app = Flask('server')
CORS(app) #disable CORS

#about Section
@app.route("/api/about")
def about():
    me = {
        "first": "Naqui",
        "last": "Darby"
    }
    return json.dumps(me)  # parse into json, then return

#Catalog Section
@app.route("/api/catalog")
def get_catalog():
    cursor = db.products.find({}) #get all
    all_products = []

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        all_products.append(prod)

    return json.dumps(all_products)    


@app.post("/api/catalog")
def save_product():
    product = request.get_json()
    db.products.insert_one(product)

    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "Title should contains at least 5 chars.")

    if not "unitPrice" in product:
        return abort(400, "Price is required.")    

    if not type(product["unitPrice"]) != float and type(product["unitPrice"]) != int:
        return abort(400, "Must be a valid number.")

    if product["unitPrice"] <= 0:
        return abort(400, "Must be higher than 0.")

    if not "image" in product or len(product["image"]) < 1:
        return abort(400, "Image is required.")

    if not "category" in product or len(product["category"]) < 1:
        return abort(400, "Category is required.")   

    if not type(product["category"]) not in [type(float),type(int)]:
        return abort(400, "number is with category required.")                


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

#Product Section
@app.route("/api/products/<id>")
def find_product(id):
    prod = db.products.find_one({"_id": ObjectId(id)})


    
    if not ObjectId.is_valid(id):
        return abort(400, "ObjectId is not an ID.") 

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

#Coupon Code Section

#Get Coupon Codes
@app.get("/api/couponCode")
def get_coupon():

    cursor= db.couponCode.find({})
    results= []

    for coupon in cursor:
        coupon["_id"] = str(coupon["_id"]) 
        results.append(coupon)
        
    return json.dumps(results)

#Valid Coupon codes
@app.get("/api/couponCode/<code>")
def get_by_code_coupon(code):

    coupon = db.couponCode.find_one({"code": code})
    if not coupon:
        return abort(400, "Invalid coupon code")

    
    code["_id"] = str(code["_id"]) 
    return json.dumps(coupon)

#Post Coupon Code
@app.post("/api/couponCode")
def save_coupon():
    coupon = request.get_json()

    if not "code" in coupon or len(coupon["code"]) < 5:
        return abort(400, "Code is required and should contains at least 5 chars.")
    
    if not "discount" in coupon:
        return abort(400, "Discount is required.")

    if type(coupon["discount"]) != int and type(coupon["discount"]) != float:
        return abort(400, "Discount is required and should a valid number.")
        
    if coupon["discount"] < 0 or coupon["discount"] > 31:
        return abort(400, "Discount should be lower than 31.")

    db.couponCode.insert_one(coupon)
    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)


app.run(debug=True)
