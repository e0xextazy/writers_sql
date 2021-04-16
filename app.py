import os
import argparse
from flask import Flask
from db import create_tables, fill_tables, get_writer_info

parser = argparse.ArgumentParser()
parser.add_argument('--init', type=bool, default=False, help='If "True" init data base.')
args = parser.parse_args()
if args.init is True:
    create_tables()
    fill_tables()

app = Flask(__name__)

@app.route('/ready')
def ready():
    return 'OK'

@app.route('/writers/<writer_id>', methods=['GET'])
def get_writter(writer_id):
    return get_writer_info(writer_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)
