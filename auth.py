from flask import Flask, request 

from flask_restful import Resource, Api, reqparse

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

todos = {}

parser = reqparse.RequestParser()
parser.add_argument('task', type=str, help='Task cannot be blank')
parser.add_argument('due_date', type=str, required=False)

class TodoList(Resource):
    def get (self):
        return todos
    def post(self):
        args = parser.parse_args()
        todo_id = len(todos) + 1
        todos[todo_id] = {'task': args['task'], 'due_date': args.get('due_date')}
        return {todo_id: todos[todo_id]}, 201
    
class TodoResources(Resource):
    def get(self, todo_id):
        if todo_id not in todos:
            return {'message': 'todo not found'}, 404
        return {todo_id: todos[todo_id]}
    def put(self, todo_id):
        args = parser.parse_args()
        if todo_id not in todos:
            return {'message': 'todo not found'}, 404
        todos[todo_id] = {'task': args['task'], 'due_date': args.get('due_date')}
        return {todo_id: todos[todo_id]}
    
    def delete(self, todo_id):
        if todo_id not in todos:
            return {'message': 'todo not found'}, 404
        del todos[todo_id]
        return '', 204
    
api.add_resource(TodoList, '/todos')
api.add_resource(TodoResources, '/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
        
