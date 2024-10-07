from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order.
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])  # Serializing messages to JSON

# POST /messages: creates a new message with a body and username from params
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()  # Getting JSON data from request
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return make_response(jsonify(new_message.to_dict()), 201)  # Returning the newly created message

# PATCH /messages/<int:id>: updates the body of the message using params
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)  # Getting message or return 404 if not found
    data = request.get_json()  # Getting JSON data from request
    message.body = data.get('body', message.body)  
    db.session.commit()
    return jsonify(message.to_dict())  # Returning the updated message

# DELETE /messages/<int:id>: deletes the message from the database
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)  # Getting message or return 404 if not found
    db.session.delete(message)
    db.session.commit()
    return make_response('', 204)  

if __name__ == '__main__':
    app.run(port=5555)
