from flask import Flask, request 

from flask_restful import Resource, Api

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

users = {}

class User(Resource):
    def get(self):
        return users
    
    def post(self):
        user_id = len(users) + 1
        users[user_id] = request.json['users_name']
        users["email"] = request.json['email']
        return {user_id: users[user_id], "email": users["email"]}, 201
    
   
    
class UserResource(Resource):
     def get (self, user_id):
         return users[user_id]

     def put(self, user_id):
        users[user_id] = request.json['users_name']
        users["email"] = request.json['email']
        return {user_id: users[user_id], "email": users["email"]}, 200
     
     def delete(self, user_id):
        del users[user_id]
        return '', 204
     

api.add_resource(User, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)