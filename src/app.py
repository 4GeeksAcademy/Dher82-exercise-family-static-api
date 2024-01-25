"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Response
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


Jhon = jackson_family.add_member(member={
    'first_name': 'John',
    'age': 33,
    'id': 12,
    'lucky_numbers': [7, 13, 22]
})

Jane = jackson_family.add_member(member={
    'first_name': 'Jane',
    'age': 35,
    'id': 5652,
    'lucky_numbers': [10, 14, 3]
})

Jimmy = jackson_family.add_member(member={
    'first_name': 'Jimmy',
    'age': 5,
    'id': 565662,
    'lucky_numbers': [1]
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

@app.route('/member', methods=['POST'])
def add_member():
    try:
        first_name =  request.json.get('first_name')
        age = request.json.get('age')
        lucky_numbers = request.json.get('lucky_numbers')
        id = request.json.get('id')

        if first_name and age and lucky_numbers :
            new_member = {
                'first_name': first_name,
                'id': id,
                'age': age,
                'lucky_numbers': lucky_numbers,
            }
            new_memberx = jackson_family.add_member(member= new_member)
            
            return jsonify(new_member), 200
        else :
            return jsonify({'fill all inputs'}), 400
    except :
        return jsonify({'msg': 'fill all'}), 500
    

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    single_obj = jackson_family.get_member(id)
    return jsonify(single_obj), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    single_obj = jackson_family.delete_member(id)

    return jsonify({'done': True}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)












