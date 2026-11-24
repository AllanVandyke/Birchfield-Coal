from flask import Flask, jsonify, request
from apiflask import APIFlask, abort
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from flask.views import View, MethodView
from flask_pymongo import PyMongo
from bson import ObjectId
from bson.errors import InvalidId
import os
from urllib.parse import quote_plus

app = APIFlask(__name__)
mongo_user = quote_plus(os.environ["MONGO_USER"])
mongo_password = quote_plus(os.environ["MONGO_PW"])
app.config["MONGO_URI"] = (
    f"mongodb://{mongo_user}:{mongo_password}@mongodb:27017/Coal_Blends?authSource=admin"
)

mongo = PyMongo(app)

CoalBlends = mongo.db.Blends
Persons = mongo.db.Persons


@app.get('/')
def index():
    return {'status': 'Healthy', 'message': 'API is running'}, 200


@app.get("/collection")
def get_collection():
    documents = [
    {**doc, "ID": str(doc["_id"])} 
    for doc in CoalBlends.find()
    ]
    for doc in documents:
            doc.pop("_id", None)
    return {"Blends": documents}, 200


@app.get("/blend/<string:item_id>")
def get_item(item_id):
    try:
        oid = ObjectId(item_id)
    except InvalidId:
        return {"message": "Invalid item ID format"}, 400
    blend = CoalBlends.find_one({'_id': oid}, {'_id': 0}) 
    if blend is None:
        return {"message": "Blend not found"}, 404
    return {"Blend": blend}, 200


@app.post("/blend")
def create_blend():
    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400
    required_fields = ["CUSTOMER", "BLEND", "PRODUCT-1", "PRODUCT-2", "PRODUCT-1-PERCENTAGE", "PRODUCT-2-PERCENTAGE"]
    for field in required_fields:
        if field not in data:
            return {"message": f"Missing required field: {field}"}, 400
    CoalBlends.insert_one(data)
    return {"New Blend": data}, 201


@app.patch("/blend/<string:item_id>")
def update_blend(item_id):
    try:
        oid = ObjectId(item_id)
    except InvalidId:
        return {"message": "Blend not found"}, 404
    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400
    result = CoalBlends.update_one({'_id': oid}, {'$set': data})
    if result.matched_count == 0:
        return {"message": "Blend not found"}, 404
    updated_blend = CoalBlends.find_one({'_id': oid}, {'_id': 0})
    return {"Updated Blend": updated_blend}, 200


@app.delete("/blend/<string:item_id>")
def delete_blend(item_id):
    try:
        oid = ObjectId(item_id)
    except InvalidId:
        return {"message": "Blend not found"}, 404
    result = CoalBlends.delete_one({'_id': oid})
    if result.deleted_count == 0:
        return {"message": "Blend not found"}, 404
    return {"message": "Blend deleted successfully"}, 200


# -----------------------------------------------------------------------------------------------

@app.get("/Persons")
def get_all_persons():
    persons = list(Persons.find({}))
    return {"People": persons}, 200

@app.get("/Persons/count")
def get_persons_count():
    count = Persons.count_documents({})
    return {"Number of People in Collection": count}, 200

@app.get("/Persons/age/<string:age>")
def get_person_age(age):
    results = []
    try:
        for person in Persons.find({"age": int(age)}):
            results.append(person)
        if len(results) == 0:
            return {"message": "No people match that age"}
        return {"results": results}, 200
    except KeyError:
        return {"message": "Invalid age format"}, 400


@app.input(Persons)
@app.get("/Persons/ne_eye_colour/<string:eye_colour>")
def get_person_eyes(eye_colour):
    try:
        people = Persons.find_one({"eyeColor": {"$eq": eye_colour}})
        return {"Eye Colour": people}, 200  
    except KeyError:
        return {"message": "Check spelling of eye colour"}, 400
    

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.run()

