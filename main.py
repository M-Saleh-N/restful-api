from flask import Flask, request 

from flask_restful import Resource, Api

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)



todos = {}

class TodoList(Resource):
    def get(self):
        return todos
    def post(self):
        todo_id = len(todos) + 1
        todos[todo_id] = request.json['task']
        return {todo_id: todos [todo_id]}, 201
class TodoResources(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}
    def put(self, todo_id):
        todos[todo_id] = request.json['task']
        return {todo_id: todos[todo_id]}
    def delete(self, todo_id):
        del todos[todo_id]
        return '', 204
api.add_resource(TodoList, '/todos')
api.add_resource(TodoResources, '/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)