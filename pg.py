from flask import Flask, request , jsonify

from flask_restful import Resource, Api, reqparse

from flask_sqlalchemy import SQLAlchemy
import os 


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {"task": self.task, "due_date": self.due_date}
parser = reqparse.RequestParser()
parser.add_argument('task', type=str, required=True, help="Task cannot be blank")
parser.add_argument('due_date', type=str, required=True, help="Due date cannot be blank")

class TodoList(Resource):
    def get(self):
        todos = Todo.query.all()
        return {todo.id: todo.to_dict() for todo in todos}
    def post (self):
        args = parser.parse_args()
        todo = Todo(task=args['task'], due_date=args['due_date'])
        db.session.add(todo)
        db.session.commit()
        return {todo.id: todo.to_dict()}, 201
    
class TodoResource(Resource):
    def get(self, todo_id):
        todo = Todo.query.get(todo_id)
        if todo is None:
            return {'error': 'todo not found'}, 404
        return {todo.id: todo.to_dict()}
    def put (self, todo_id):
        args = parser.parse_args()
        todo = Todo.query.get(todo_id)
        if todo is None:
            return {'error': 'todo not found'}, 404
        todo.task = args['task']
        todo.due_date = args['due_date']
        db.session.commit()
        return {todo.id: todo.to_dict()}
    def delete(self, todo_id):
        todo = Todo.query.get(todo_id)
        if todo is None:
            return {'error': 'todo not found'}, 404
        db.session.delete(todo)
        db.session.commit()
        return ' ', 204
    
#---Route---
api.add_resource(TodoList, '/todos')
api.add_resource(TodoResource, '/todos/<int:todo_id>')

#---main---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

