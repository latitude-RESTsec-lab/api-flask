#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

@author: unbdev
"""

import json
import collections

from conexao import Conexao

stmt =      """
            select s.id_servidor, s.siape, s.id_pessoa, s.matricula_interna, 
                   s.id_foto, s.nome_identificacao, 
                   p.nome, p.data_nascimento, p.sexo
            from rh.servidor s
            inner join comum.pessoa p on (s.id_pessoa = p.id_pessoa) and (p.tipo = 'F')
            """

def buscar_dados(): 
    conn = Conexao('vml4unb001', 'administrativo', 'sipac', '1qaz2wsxsipac')
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



from flask import Flask

app = Flask(__name__)

@app.route('/api/servidores', methods=['GET'])
def get_servidores():
    dados = buscar_dados()
    j = json.dumps(dados)
    return j

app.run(debug=True, host='0.0.0.0', port=8000)
