from flask import Flask, jsonify, request
import json 
from db import get_db
from bson.objectid import ObjectId

app = Flask(__name__)
db = get_db()
col = db["items"]

'''
=== Data Scheme ============
item = {
	_id: ObjectId(),
	productName: "tshirt",
	variants: [
		{
			size: "M",
			colour: "Ferrari Red",
			material: "Cotton",
		}
		{
			size: "XL",
			colour: "Navy Blue",
			material: "Polyester",
		}
	]
}

=== API Endpoints ============
GET /items
GET /item?id
POST /item
POST /items
PATCH /item?id
'''

init_data = [
	{
		"productName": "Shirt",
		"variants": [
			{
				"size": "S",
				"colour": "Red",
				"material": "Cotton"
			},
			{
				"size": "S",
				"colour": "Green",
				"material": "Cotton"
			},
			{
				"size": "M",
				"colour": "Red",
				"material": "Cotton"
			},
			{
				"size": "M",
				"colour": "Green",
				"material": "Cotton"
			},
		]
	}
]

@app.route('/api/items/', methods=['GET'])
def getItems():
		if request.method == 'GET':
			# col.insert_many(init_data)
			data = list(col.find())
			for docs in data:
				docs["_id"] = str(docs["_id"])
			return jsonify(data)

@app.route('/api/item/', methods=['GET'])
def getItem():
		if request.method == 'GET':
			try:
				objId = ObjectId(request.args.get("id"))
				data = col.find_one({"_id": objId})
				if (data == None): return "Item does not exist"
				data = dict(data)
				data["_id"] = str(data["_id"])
				return jsonify(data)
			except:
				return "Invalid ObjectId"

@app.route('/api/items/', methods=['POST'])
def addItems():
		if request.method == 'POST':
			data = request.get_json()
			res = col.insert_many(data);
			inserted_ids = [str(_id) for _id in res.inserted_ids]
			return jsonify({"inserted_ids": inserted_ids})

@app.route('/api/item/', methods=['POST'])
def addItem():
		if request.method == 'POST':
			data = request.get_json()
			res = col.insert_one(data);
			return jsonify({"inserted_id": str(res.inserted_id)})

@app.route('/api/item/', methods=['PATCH'])
def updateItem():
		if request.method == 'PATCH':
			data = request.get_json()
			_id = ObjectId(request.args.get("id"))
			res = col.update_one({"_id": _id}, {"$set": data});
			return jsonify({"matched_count": str(res.matched_count), "modified_count": str(res.modified_count)})
