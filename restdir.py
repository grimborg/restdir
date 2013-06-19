from flask import Flask, request
from opster import command
from glob import glob
import json

filetypes = '*.html'

app = Flask(__name__)

@app.after_request
def after(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods',
                         'POST, GET, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, X-Requested-With')
    response.headers.add('Access-Control-Max-Age', '1728000')

    return response

@app.route('/')
def handle_root():
    return json.dumps(glob(filetypes))


@app.route('/<filename>', methods=['GET', 'PUT', 'POST'])
def handle_file(filename):
    if '/' in filename:
        raise Exception
    if request.method == 'GET':
        with open(filename, 'r') as f:
            return f.read()
    elif request.method in ('PUT', 'POST'):
        print 'writing to ',filename
        with open(filename, 'w') as f:
            f.write(request.data)
        return 'OK'

@command()
def serve():
    app.run(debug=True)


