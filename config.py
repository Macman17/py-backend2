from http import client
import imp
import pymongo
import certifi


con_str = "mongodb+srv://Naqui17:Mackman1113!!!!@cluster0.nakll.mongodb.net/SweetLu?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCafile=certifi.where())

db = client.get_database("SweetLu")
