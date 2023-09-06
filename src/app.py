"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# // crear mis empoints



@app.route('/members', methods=['GET'])
def handle_hello():

    # estructura de datos de familia llamado a sus metodos
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#2 obtener un solo  de la familia

@app.route('/member/<int:member_id>', methods=['GET'])
def get_single_member(member_id):


    # Hago una consulta a la tabla FamilyStructure para que traiga un miembro de la familia
    member = jackson_family.get_member(member_id)

    # Responde mostrando el miembro consultado

    return jsonify(member), 200

# 3 Añadir un miembro a la familia

@app.route('/member', methods=['POST'])
def add_member():
    new_member=json.loads(request.data)
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

# 3 Borrar un miembro a la familia
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):

    jackson_family.delete_member(member_id)

    return jsonify({"done": True}), 200




    




    








# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
