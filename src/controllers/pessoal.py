#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:46:12 2018

"""

import json
from flask import Blueprint, request

import db.db as db

def validate_suported_mime_type():
    if 'Accept' in request.headers:
        if request.headers['Accept'] == '*/*':
            return True
        else:
            return request.headers['Accept'] == 'application/json'
    else:
        return True

# stores all database configuration
database_config = {}

# operations to be registered in the application object
pessoal_controllers = Blueprint('pessoal_controllers', __name__)


def configure_params(p_servername, p_database, p_username, p_password):
    database_config['db_servername'] = p_servername
    database_config['db_database'] = p_database
    database_config['db_username'] = p_username
    database_config['db_password'] = p_password

# web service API servidores
@pessoal_controllers.route('/api/servidores', methods=['GET'])
def get_all_employees_api():
    dados = db.get_all_employees(database_config)
    j = json.dumps(dados)
    return j, {'Content-Type': 'application/json; charset=utf-8'}

# web service API servidor/{matricula}
@pessoal_controllers.route("/api/servidor/<int:mat_servidor>", methods = ['GET'])
def get_employee_by_id_api(mat_servidor=None):
    if not validate_suported_mime_type():
        return "Unsupported Media Type", 415
    elif request.method == "GET":
        if mat_servidor:
            # retrieve one specific employee
            dados = db.get_employee_by_id(database_config, 
                                          mat_servidor)
            if dados:
                return json.dumps(dados), {'Content-Type': 'application/json; charset=utf-8'}
            else:
                return "Not found", 404
        else:
            return "Bad Request", 400

# web service - create new employee
@pessoal_controllers.route('/api/servidor', methods=['POST'])
def create_a_new_employee_api():
    '''API to create a new employee record using the provided data.

    Requires JSON formatted request containing the employ data listed 
    below in the sample_json var.
	
    Example: 
	curl -H "Content-Type: application/json" -X POST -d '{"id_servidor": 4321, "siape": 123456, "id_pessoa": 1234, "matricula_interna": 54321, "nome": "João da Silva", "data_nascimento": "1970-01-31", "sexo": "M"}' http://localhost:8000/api/servidor/
    
    sample_json = {
	"id_servidor": 4321,
	"siape": 123456,
	"id_pessoa": 1234,
	"matricula_interna": 54321,
	"nome": "João da Silva",
	"data_nascimento": "1970-01-31",
	"sexo": "M"
}
	'''
    if not validate_suported_mime_type():
        return "Unsupported Media Type", 415

    # TODO test if the data is JSON
    new_employee_data = request.json
    print "post de servidor={}".format(new_employee_data)

    data_validation = dict()
    data_validation['required'] = __required_data_validator(new_employee_data)
    if data_validation['required']:
        return "Bad request\n{}".format(data_validation['required']), 400

    #if 
    # TODO validations:
    # - date validator: data_nascimento
    # - int validator: id_servidor, siape, id_pessoa
    # - size validator: nome, sexo
    # - domain validator: sexo
    # - business validator: data_nascimento


    return "Ok", 200

def __required_data_validator(employee_data):
    '''Function to validate if all required data is present.

    parameter
        - employee_data: a dict with the reveived data.

    returns
        - Empty object: if it is all ok
        - Message with the missing fields: if is not ok
	'''
    required_data = ['nome', 'siape', 'data_nascimento', 'sexo', 'id_servidor', 'id_pessoa']
    diff_result = set(required_data) - set(employee_data)

    if not diff_result:
        return None
    else:
        message = "This required data is missing: {}".format(diff_result)
        return message
