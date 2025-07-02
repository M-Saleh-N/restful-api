from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# --- Flask App Initialization ---
app = Flask(__name__)
api = Api(app)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:657844@localhost:5432/tododb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Model Definition ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }

# --- Parser for User Inputs ---
parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, required=True, help="First name cannot be blank")
parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank")
parser.add_argument('email', type=str, required=True, help="Email cannot be blank")
parser.add_argument('password', type=str, required=True, help="Password cannot be blank")

# --- Resource: User List + Create ---
class UserList(Resource):
    def get(self):
        users = User.query.all()
        return {user.id: user.to_dict() for user in users}

    def post(self):
        args = parser.parse_args()
        hashed_password = bcrypt.hashpw(args['password'].encode('utf-8'), bcrypt.gensalt())
        user = User(
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            password=hashed_password.decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        return {user.id: user.to_dict()}, 201

# --- Resource: Individual User ---
class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return {'error': 'User not found'}, 404
        return {user.id: user.to_dict()}

    def put(self, id):
        args = parser.parse_args()
        user = User.query.get(id)
        if user is None:
            return {'error': 'User not found'}, 404
        user.first_name = args['first_name']
        user.last_name = args['last_name']
        db.session.commit()
        return {user.id: user.to_dict()}

    def delete(self, id):
        user = User.query.get(id)
        if user is None:
            return {'error': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return '', 204

# --- Routes ---
api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/users/<int:id>')

# --- Main App Runner ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
