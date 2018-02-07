# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

"""

from flask import Flask
import argparse
import logging
import os
import json

import controllers.pessoal as con


app = Flask(__name__)
app.register_blueprint(con.pessoal_controllers)

def load_configuration(config_file):
    filename = config_file
    if not os.path.dirname(os.path.dirname(config_file)):
        filename = os.path.dirname(__file__) + "/" + config_file

    if not os.path.isfile(filename):
        logging.error("Database config file is missing")
        # TODO raise exception

    configuration = json.load(open(filename))
    return configuration

if __name__ == '__main__':
    # configuring the parameters parser and storing parameters in global vars
    parser = argparse.ArgumentParser(description='"API Servidor" to provide/handle employee\'s data.')
    parser.add_argument("-c", "--config", 
                        help="Database config file path", metavar="config_file")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--no-ssl", action="store_true", 
                        help='Start server without SSL')
    args = parser.parse_args()

    server_config = {}
    if args.config:
        server_config = load_configuration(args.config)
    con.configure_params(server_config['servername'], server_config['database'], server_config['username'], server_config['password'])

    APP_LOG_FILENAME = os.path.dirname(__file__) + "/" + server_config['LogLocation']

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(filename=APP_LOG_FILENAME,
                        filemode='a',
                        format='%(asctime)s,%(msecs)-3d - %(name)-12s - %(levelname)-8s => %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=log_level)
    logging.info("API Employee started")

    if args.no_ssl:
        server_port = server_config['HttpPort']
        server_protocol = 'http'
        ssl_config = None
    else:
        server_port = server_config['HttpsPort']
        server_protocol = 'https'
        ssl_config = (server_config['TLSCertLocation'], server_config['TLSKeyLocation'])
    print("API service is starting and will be avaialble at '{}://localhost:{}/.\nThe application log is stored in the file '{}'.".format(server_protocol, server_port, APP_LOG_FILENAME))

    # starting the web server
    app.run(debug=args.debug, host='0.0.0.0', port=server_port, ssl_context=ssl_config)
