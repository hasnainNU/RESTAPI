from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#creat database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False) 
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

#converting the above model into a json 
def to_dict(self):
    return {
        "id": self.id,
        "destination": self.destination,
        "name": self.name,
        "description": self.description
    }

#context manager to create the database tables
with app.app_context():
    db.create_all()
#create routes




#create a route to get all destinations
@app.route('/')
def home ():
    return jsonify('Welcome to the Flask App!') 

@app.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

@app.route('/destinations/<int:destination_id>', methods=['POST'])
def create_destination(destination_id):
    if destination:
        return jsonify({'message': 'Destination already exists'}), 400
    else:
        return jsonify({'error': 'Destination not found '}), 404 
    
#post request to create a new destination
@app.route('/destinations', methods=['POST'])
def create_destination():
    data = request.get_json()
    new_destination = Destination(
        destination=data['destination'],
        name=data['name'],
        description=data['description']
    )
    #insert the new destination into the database
    db.session.add(new_destination)
    db.session.commit()
    return jsonify(new_destination.to_dict()), 201
if __name__ == '__main__':
    app.run(debug=True)