#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

"""

from flask import Flask
import argparse

import controllers.pessoal as con

app = Flask(__name__)
app.register_blueprint(con.pessoal_controllers)

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

    con.configure_params(args.servername, args.database, args.username, args.password)

    # starting the web server
    app.run(debug=True, host='0.0.0.0', port=8000)
