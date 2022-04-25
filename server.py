
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
# start the server
app.run(debug=True)
