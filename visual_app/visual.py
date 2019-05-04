from flask import Flask, request, redirect, url_for, render_template
from flask import make_response, jsonify
import flask
import json
import redis

app = Flask(__name__)
redis_store = redis.Redis('localhost')

@app.route('/error/<err_number>')
def error(err_number):
    message = {
        'status': 'error'
    }
    if err_number == '1':
        message['message'] = "No such page."
    elif err_number == '2':
        message['message'] = "Wrong method."
    else:
        message['message'] = "Bad Request. Probably you forgot double quotes."
    return make_response(jsonify(message), 404)

@app.route('/')
def welcome():
    return render_template('welcome.html', add=add_new_list(), show=show_lists())

@app.errorhandler(400)
def bad_request(e):
    return error(3)

@app.errorhandler(405)
def page_not_found(e):
    return error(1)

def show_lists():
    keys = redis_store.keys()
    values = redis_store.mget(keys)
    db = dict(zip(keys, values))
    if (len(db) == 0):
        db = None
    return render_template('display.html', db=db)

def add_new_list():
    if (request.method == 'POST'):
        name = request.form['name']
        values = request.form['values']
        for_db = dict([(name, values)])
        js = json.dumps(for_db)
        redis_store.set(name, values)
        return make_response(jsonify(js), 200)
    elif (request.method == 'GET'):
        return render_template('add_new_list.html')
    else:
        return error(2)

def clear_data_base():
    keys = redis_store.keys()
    for key in keys:
        redis_store.delete(key)
    return make_response(jsonify("status: cleared database"), 200)

@app.route('/<name>', methods=['POST', 'GET'])
def main(name):
    if (name == "add_new_list"):
        return add_new_list()
    elif (name == "show_lists"):
        return show_lists()
    elif (name == "delete"):
        return clear_data_base()
    else:
        return redirect(url_for('error', err_number = 1))

if __name__ == "__main__":
    app.run(debug=True)
