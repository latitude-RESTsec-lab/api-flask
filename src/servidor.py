#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

@author: unbdev
"""

import json
import collections
from flask import Flask, request
import argparse

from conexao import Conexao

stmt_all_emp = """
            select s.id_servidor, s.siape, s.id_pessoa, s.matricula_interna, 
                   s.id_foto, s.nome_identificacao, 
                   p.nome, p.data_nascimento, p.sexo
            from rh.servidor s
            inner join comum.pessoa p on (s.id_pessoa = p.id_pessoa) and (p.tipo = 'F')
            """
stmt_one_emp = stmt_all_emp + "where s.siape = {}"

db_servername = ''
db_database = ''
db_username = ''
db_password = ''

# get all employees from database, using the Conexao object
def get_all_employees(servername, database, username, password):
    conn = Conexao(servername, database, username, password)
    rows = conn.consultar(stmt_all_emp)

    # Convert query to row arrays
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id_servidor'] = row[0]
        d['siape'] = row[1]
        d['id_pessoa'] = row[2]
        d['matricula_interna'] = row[3]
        d['nome'] = row[6]
        d['data_nascimento'] = row[7].__str__()
        d['sexo'] = row[8]
        objects_list.append(d)

    conn.fechar()
    
    return objects_list

# get on employee from database, using the Conexao object
def get_employee_by_id(servername, database, username, password, mat_servidor):
    conn = Conexao(servername, database, username, password)
    rows = conn.consultar(stmt_one_emp.format(mat_servidor))

    employee_data = {}
    if not rows:
        return None
    else:
        # Convert query to row arrays
        for row in rows:
            employee_data = collections.OrderedDict()
            employee_data['id_servidor'] = row[0]
            employee_data['siape'] = row[1]
            employee_data['id_pessoa'] = row[2]
            employee_data['matricula_interna'] = row[3]
            employee_data['nome'] = row[6]
            employee_data['data_nascimento'] = row[7].__str__()
            employee_data['sexo'] = row[8]

    conn.fechar()
    
    return employee_data

def validate_suported_mime_type():
    # TODO aceitar '*/*'
    #if 'Accept' in request.headers and not request.headers['Accept'] == 'application/json':
    if 'Accept' in request.headers:
        if request.headers['Accept'] == '*/*':
            return True
        else:
            return request.headers['Accept'] == 'application/json'
    else:
        return True


app = Flask(__name__)

# web service API servidores
@app.route('/api/servidores', methods=['GET'])
def get_all_employees_api():
    dados = get_all_employees(db_servername, db_database, db_username, db_password)
    j = json.dumps(dados)
    return j, {'Content-Type': 'application/json; charset=utf-8'}

# web service API servidor/{matricula}
@app.route("/api/servidor/<int:mat_servidor>", methods = ['GET'])
def get_employee_by_id_api(mat_servidor=None):
    if not validate_suported_mime_type():
        return "Unsupported Media Type", 415
    elif request.method == "GET":
        if mat_servidor:
            # retrieve one specific employee
            dados = get_employee_by_id(db_servername, db_database, db_username, db_password, mat_servidor)
            if dados:
                return json.dumps(dados), {'Content-Type': 'application/json; charset=utf-8'}
            else:
                return "Not found", 404
        else:
            return "Bad Request", 400


if __name__ == '__main__':
    # configuring the parameters parser and storing parameters in global vars
    parser = argparse.ArgumentParser(description='API Servidor to provide employee\'s data.')

    parser.add_argument("-s", "--servername", metavar='server_name', 
                        help='Name of the database_server')
    parser.add_argument("-d", "--database", 
                        help="Name of the database", metavar="database_name")
    parser.add_argument("-u", "--username", 
                        help="Username to access the database", metavar="username")
    parser.add_argument("-p", "--password", 
                        help="User's password to acess the database", metavar="user_password")
    args = parser.parse_args()
    db_servername = args.servername
    db_database = args.database
    db_username = args.username
    db_password = args.password

    # starting the web server
    app.run(debug=True, host='0.0.0.0', port=8000)
