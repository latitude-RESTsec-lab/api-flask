#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

@author: unbdev
"""

from conexao import Conexao


def conexao_direta():
    con = Conexao('vml4unb001', 'administrativo', 
                  'sipac', '1qaz2wsxsipac')
    stmt = "select * from rh.servidor "
    res = con.consultar(stmt)
    for rec in res:
        print (rec)
    con.fechar()

def conexao_webservice():
    app.run(debug=True)



from flask import Flask
import simplejson as json

app = Flask(__name__)

@app.route('/api/servidores', methods=['GET'])
def get_servidores():
    con = Conexao('vml4unb001', 'administrativo', 
                  'sipac', '1qaz2wsxsipac')
    stmt = "select * from rh.servidor "
    res = con.consultar(stmt)
    con.fechar()
    return json({'dados':res})


conexao_webservice()
