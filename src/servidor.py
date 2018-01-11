#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

@author: unbdev
"""

import json
import collections
from flask import Flask
import argparse

from conexao import Conexao

stmt =      """
            select s.id_servidor, s.siape, s.id_pessoa, s.matricula_interna, 
                   s.id_foto, s.nome_identificacao, 
                   p.nome, p.data_nascimento, p.sexo
            from rh.servidor s
            inner join comum.pessoa p on (s.id_pessoa = p.id_pessoa) and (p.tipo = 'F')
            """
db_servername = ''
db_database = ''
db_username = ''
db_password = ''

def buscar_dados(servername, database, username, password):
    conn = Conexao(servername, database, username, password)
    rows = conn.consultar(stmt)
 
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
 
    #j = json.dumps(objects_list)
    #objects_file = 'student_objects.js'
    #f = open(objects_file,'w')
    #f.write(j)
    #f.close()
    #print "&gt;&gt;", f, j
 
    conn.fechar()
    
    return objects_list

app = Flask(__name__)

@app.route('/api/servidores', methods=['GET'])
def get_servidores():
    dados = buscar_dados(db_servername, db_database, db_username, db_password)
    j = json.dumps(dados)
    return j

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='API Servidor to provide servants\' data.')

    parser.add_argument("-s", "--servername", metavar='server name', #type=string, #nargs='+',
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

    app.run(debug=True, host='0.0.0.0', port=8000)
