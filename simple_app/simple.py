from flask import Flask, request, make_response, jsonify
from redis import Redis
import json
import redis

app = Flask(__name__)
redis_store = redis.Redis('localhost')

def error(err_number):
    message = {
        'status': 'error',
    }
    if err_number == 1:
        message['message'] = 'Wrong method!'
    elif err_number == 2:
        message['message'] = 'Wrong content type!'
    elif err_number == 3:
        message['message'] = 'Bad Request. Probably you forgot double quotes.'
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(400)
def bad_request(e):
    return error(3)

@app.errorhandler(405)
def page_not_found(e):
    return error(1)

@app.route('/')
def welcome():
    return make_response(jsonify("Welcome!"))

def add_new_list():
    if request.headers['Content-Type'] == 'application/json':
        if request.method == "POST":
            new_lst = request.json
            name = "".join(map(str, list(new_lst.keys())))
            values = "".join(map(str, list(new_lst.values())))
            redis_store.set(name, values)
            return make_response(jsonify("status: ok"))
        else:
            return error(1)
    else:
        return error(2)

def show_lists():
    keys = redis_store.keys()
    values = redis_store.mget(keys)
    db = str(dict(zip(keys, values)))
    return make_response(jsonify(db))

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
    else:
        return make_response(jsonify("error"), 404)

if __name__ == "__main__":
    app.run(debug=True)