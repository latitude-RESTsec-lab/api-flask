#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:46:12 2018

"""

import json
from flask import Blueprint, request
from datetime import datetime
import re

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
    # - required data
    data_validation['required'] = __required_data_validator(new_employee_data)
    # - size validator: nome, sexo
    data_validation['size'] = __data_size_validator(new_employee_data)
    # - domain validator: sexo
    data_validation['domain'] = __data_domain_validator(new_employee_data)
    # - business validator: data_nascimento
    data_validation['business'] = __business_rule_validator(new_employee_data)
    # - regex validator: date (data_nascimento), int (id_servidor, siape, id_pessoa)
    data_validation['regex'] = __regex_validator(new_employee_data)

    msg = ";\n".join(list(str(v) for k, v in data_validation.iteritems() if v))
    if msg:
        return "Bad request.\n{}".format(msg), 400

    # TODO save data in the database

    return "Created", 201

def __regex_validator(employee_data):
    '''TODO.

    parameter
        - employee_data: a dict with the reveived data.

    returns
        - Empty object: if it is all ok
        - Message with the fields with wrong values: if is not ok
	'''
    INT_VALIDATION_PATTERN = r'\b[0-9]+\b'
    result = []

    for x in ['id_servidor', 'siape', 'id_pessoa']:
        print x, employee_data[x]
        if x in employee_data and not re.search(INT_VALIDATION_PATTERN, str(employee_data[x])):
            result.append("'{}' is an unaccepted pattern for the field '{}'".format(employee_data[x], x))

    return "; ".join(result)

def __business_rule_validator(employee_data):
    '''TODO.

    parameter
        - employee_data: a dict with the reveived data.

    returns
        - Empty object: if it is all ok
        - Message with the fields with wrong values: if is not ok
	'''
    result = []
    
    if 'data_nascimento' in employee_data:
        data_nascimento = datetime.strptime(employee_data['data_nascimento'], '%Y-%m-%d')
        if data_nascimento > datetime.now():
            result.append("Field '{}' has an unaccepted value: {}".format('data_nascimento', 'this date should be in the past'))

    return "; ".join(result)

def __data_domain_validator(employee_data):
    '''Function to validate if a subset of fields has accepted values.

    parameter
        - employee_data: a dict with the reveived data.

    returns
        - Empty object: if it is all ok
        - Message with the fields with wrong data: if is not ok
	'''
    result = []
    domain_data = [('sexo', {'F', 'M'})]
    for x in domain_data:
        if employee_data[x[0]] not in x[1]:
            result.append("'{}' is an unaccepted value for the field {}".format(employee_data[x[0]], x[0]))
    return "; ".join(result)

def __data_size_validator(employee_data):
    '''Function to validate if a subset of fields is in an accepted size.

    parameter
        - employee_data: a dict with the reveived data.

    returns
        - Empty object: if it is all ok
        - Message with the fields in a wrong size: if is not ok
	'''
    result = []
    data_size = [('nome', 100), ('sexo', 1)]
    for x in data_size:
        if len(employee_data[x[0]]) > x[1]:
            result.append("{} is {} but it must be {}".format(x[0], len(employee_data[x[0]]), x[1]))
    return "; ".join(result)

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
        message = "This required data is missing: {}".format("; ".join(diff_result))
        return message
