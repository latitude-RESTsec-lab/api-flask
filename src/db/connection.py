#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

"""

import psycopg2

class Conexao(object):
    _db=None    

    def __init__(self, db_config):
        if not db_config:
            raise Exception("There is no database configuration.")
        elif not set(('db_servername', 'db_database', 'db_username', 'db_password')).issubset(db_config):
            raise Exception("Some database configuration is missing.")

        self._db = psycopg2.connect(host=db_config['db_servername'], 
                                    database=db_config['db_database'], 
                                    user=db_config['db_username'], 
                                    password=db_config['db_password'])

    def manipular(self, sql):
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except:
            return False
        return True

    def consultar(self, sql):
        rs=None
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            rs=cur.fetchall()
        except:
            return None
        return rs

    def proximaPK(self, tabela, chave):
        sql='select max('+chave+') from '+tabela
        rs = self.consultar(sql)
        pk = rs[0][0]  
        return pk+1

    def fechar(self):
        self._db.close()
