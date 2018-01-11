#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

@author: unbdev
"""

import json
import collections
from flask import Flask
from optparse import OptionParser

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
    parser = OptionParser()
    parser.add_option("-s", "--servername", dest="db_servername", action="store", type="string", 
                        help="Name of the database server", metavar="DB")
    parser.add_option("-d", "--database", dest="db_database", action="store", type="string", 
                        help="Name of the database", metavar="DB")
    parser.add_option("-u", "--username", dest="db_username", action="store", type="string", 
                        help="Username to access the database", metavar="DB")
    parser.add_option("-p", "--password", dest="db_password", action="store", type="string", 
                        help="Password to acess the database", metavar="DB")
    (options, args) = parser.parse_args()
    db_servername = options.db_servername
    db_database = options.db_database
    db_username = options.db_username
    db_password = options.db_password

    app.run(debug=True, host='0.0.0.0', port=8000)
