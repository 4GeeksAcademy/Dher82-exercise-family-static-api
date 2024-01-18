"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
John=jackson_family.add_member(member={
    "firt_name": "John",
    "age": 33,
    "id": 12,
    "lucky_numbers": [7, 13, 22]
})

Jane=jackson_family.add_member(member={
    "firt_name": "Jane",
    "age": 35,
    "id": 5652,
    "lucky_numbers": [10, 14, 3]
})

Jimmy=jackson_family.add_member(member={
    "firt_name": "Jimmy",
    "age": 5,
    "id": 5662,
    "lucky_numbers": [1]
})
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    

    return jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):

    # this is how you can use the Family datastructure by calling its methods
    one_member = jackson_family.get_member(id)
    
    return jsonify(one_member), 200

@app.route('/members', methods=['POST'])
def add_member():
    try:
        first_name=request.json.get("first_name")
        age=request.json.get("age")
        id=request.json.get("id")
        lucky_numbers=request.json.get("lucky_numbers")
        if first_name and age and lucky_numbers:
            new_member={
                "first_name":first_name,
                "id":id,
                "age":age,
                "lucky_numbers":lucky_numbers

            }
            new_members=jackson_family.add_member(members=new_member)

            return jsonify(new_members), 200
        else:
            return jsonify({"solicitud falló"}), 400
    except:
        return jsonify({"el servidor encontró un error"}), 500
    
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.delete_member(id)
    print (delete_member)
    if(delete_member =="no encontrado"):
       return jsonify({"msg":"no se ha podido eliminar, usuario no encontrado "}), 400
    else:
        members=jackson_family.get_all_members()
    return jsonify({"done":True , "memberrest":members}), 200    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
