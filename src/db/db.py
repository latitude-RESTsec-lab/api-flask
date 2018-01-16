#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017
@author: unbdev
"""

import collections

from connection import Conexao

stmt_all_emp = """
            select s.id_servidor, s.siape, s.id_pessoa, s.matricula_interna, 
                   s.id_foto, s.nome_identificacao, 
                   p.nome, p.data_nascimento, p.sexo
            from rh.servidor s
            inner join comum.pessoa p on (s.id_pessoa = p.id_pessoa) and (p.tipo = 'F')
            """
stmt_one_emp = stmt_all_emp + "where s.siape = {}"

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
