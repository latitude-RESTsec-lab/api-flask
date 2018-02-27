# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:46:12 2018

"""

import collections
import time, datetime
import logging
import hashlib

from db.connection import PostgresDbHelper

SQL_STMT_ALL_EMPLOYEES = """
            select s.id_servidor, s.siape, s.id_pessoa, s.matricula_interna, 
                   s.nome_identificacao, 
                   p.nome, p.data_nascimento, p.sexo
            from rh.servidor s
            inner join comum.pessoa p on (s.id_pessoa = p.id_pessoa) and (p.tipo = 'F')
            """
SQL_STMT_ONE_EMPLOYEE = SQL_STMT_ALL_EMPLOYEES + "where s.matricula_interna = {}"
SQL_STMT_NEW_EMPLOYEE = """
            INSERT INTO rh.servidor_tmp(
                nome, nome_identificacao, siape, id_pessoa, matricula_interna, 
                data_nascimento, sexo)
			VALUES ('{}', '{}', {}, {}, {}, '{}', '{}');
            """

# get all employees from database, using the PostgresDbHelper object
def get_all_employees(database_configuration):
    conn = PostgresDbHelper(database_configuration)
    rows = conn.retrieve(SQL_STMT_ALL_EMPLOYEES)

    # Convert query to row arrays
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id_servidor'] = row[0]
        d['siape'] = row[1]
        d['id_pessoa'] = row[2]
        d['matricula_interna'] = row[3]
        d['nome'] = row[5]
        d['data_nascimento'] = row[6].__str__()
        d['sexo'] = row[7]
        objects_list.append(d)

    conn.close()
    
    return objects_list

# get on employee from database, using the PostgresDbHelper object
def get_employee_by_id(database_configuration, mat_servidor):
    conn = PostgresDbHelper(database_configuration)
    rows = conn.retrieve(SQL_STMT_ONE_EMPLOYEE.format(mat_servidor))

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
            employee_data['nome'] = row[5]
            employee_data['data_nascimento'] = row[6].__str__()
            employee_data['sexo'] = row[7]

    conn.close()
    
    return employee_data

# stores a new employee in the database, using the PostgresDbHelper object
def create_employee(database_configuration, new_employee):
    conn = PostgresDbHelper(database_configuration)

    date_now = "{:%Y-%m-%dT%H:%M:%S-%z}".format(datetime.datetime.now())
    base_key = new_employee['nome'] + date_now
    b = hashlib.md5(base_key.encode('utf-8')).hexdigest()
    bid = int(b, 16)
    new_key = bid % 99999

    parsed_sql = SQL_STMT_NEW_EMPLOYEE.format(
                                    new_employee['nome'],
                                    new_employee['nome_identificacao'],
                                    new_employee['siape'],
                                    new_employee['id_pessoa'],
                                    new_key,
                                    new_employee['data_nascimento'],
                                    new_employee['sexo'])

    if not conn.persist(parsed_sql):
        logging.error("Database error!")
        conn.close()
        return None

    conn.close()
    return new_key
