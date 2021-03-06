"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, ToDoList
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/tasks', methods=['GET'])
def tasks_list():

    # get all the people
    query_task = ToDoList.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_tasks = list(map(lambda x: x.serialize(), query_task))

    return jsonify(all_tasks), 200

@app.route('/newTasks', methods=['POST'])
def addList():

    request_body = request.get_json()
    task = ToDoList(task=request_body["task"], done=request_body["done"])
    db.session.add(task)
    db.session.commit()

    return jsonify("Tarea agregada"), 200

@app.route('/del_tasks/<int:id>', methods=['DELETE'])
def del_tasks(id):

    task = ToDoList.query.get(id)
    if task is None:
        raise APIException('Task not found', status_code=404)
    db.session.delete(task)
    db.session.commit()
 
    return jsonify("Tarea eliminada"), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
