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

pessoal_controllers = Blueprint('pessoal_controllers', __name__)


def configure_params(p_servername, p_database, p_username, p_password):
    database_config['db_servername'] = p_servername
    database_config['db_database'] = p_database
    database_config['db_username'] = p_username
    database_config['db_password'] = p_password

# web service API servidores
@pessoal_controllers.route('/api/servidores', methods=['GET'])
def get_all_employees_api():
    dados = db.get_all_employees(database_config['db_servername'], 
                                 database_config['db_database'], 
                                 database_config['db_username'], 
                                 database_config['db_password'])
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
            dados = db.get_employee_by_id(database_config['db_servername'], 
                                 database_config['db_database'], 
                                 database_config['db_username'], 
                                 database_config['db_password'], mat_servidor)
            if dados:
                return json.dumps(dados), {'Content-Type': 'application/json; charset=utf-8'}
            else:
                return "Not found", 404
        else:
            return "Bad Request", 400
