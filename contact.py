from flask import Flask, request 

from flask_restful import Resource, Api

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

contacts = {}


class Contact(Resource):
    def get(self):
        return contacts
    def post(self):
        new_contact = len(contacts) + 1 
        contacts[new_contact] = request.json["contact"]
        return {new_contact: contacts[new_contact]}, 201
class ContactResource(Resource):
    def get(self, contact_id):
        return {contact_id: contacts[contact_id]}
    def put(self, contact_id):
        contacts[contact_id] = request.json["contact"]
        return {contact_id: contacts[contact_id]}
    def delete(self, contact_id):
        del contacts[contact_id ]
        return '', 204
    
api.add_resource(Contact, '/contacts')
api.add_resource(ContactResource, '/contacts/<int:contact_id>')

if __name__ == '__main__':
    app.run(debug=True)      