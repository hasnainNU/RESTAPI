from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///research.db'
db = SQLAlchemy(app)

FIELDS = [
    'Research_title', 'Research_description', 'Research_area', 'Faculty_name',
    'Departement', 'Required_skills', 'Avaliable_positions',
    'Application_deadline', 'status',
]


class Research(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Research_title = db.Column(db.String(100), nullable=False)
    Research_description = db.Column(db.String(500), nullable=False)
    Research_area = db.Column(db.String(100), nullable=False)
    Faculty_name = db.Column(db.String(100), nullable=False)
    Departement = db.Column(db.String(100), nullable=False)
    Required_skills = db.Column(db.String(200), nullable=False)
    Avaliable_positions = db.Column(db.Integer, nullable=False)
    Application_deadline = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        d = {'id': self.id}
        for f in FIELDS:
            d[f] = getattr(self, f)
        return d


with app.app_context():
    db.create_all()


def read_body():
    """Return (data, error_response). Checks all required fields exist."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, (jsonify({'message': 'Invalid JSON body'}), 400)
    missing = [f for f in FIELDS if f not in data or data[f] in (None, '')]
    if missing:
        return None, (jsonify({'message': 'Missing fields: ' + ', '.join(missing)}), 400)
    try:
        data['Avaliable_positions'] = int(data['Avaliable_positions'])
    except (TypeError, ValueError):
        return None, (jsonify({'message': 'Available positions must be a number'}), 400)
    if data['Avaliable_positions'] < 1:
        return None, (jsonify({'message': 'Available positions must be at least 1'}), 400)
    if data['status'] not in ('Open', 'Closed'):
        return None, (jsonify({'message': 'Status must be Open or Closed'}), 400)
    return data, None


# create routes
@app.route('/')
def home():
    return render_template('index.html')


# GET: all research opportunities
@app.route('/api/researchtitles', methods=['GET'])
def get_research_titles():
    items = Research.query.order_by(Research.id).all()
    return jsonify([r.to_dict() for r in items])


# GET: one research opportunity by id
@app.route('/api/researchtitles/<int:id>', methods=['GET'])
def get_research_title(id):
    research = db.session.get(Research, id)
    if research:
        return jsonify(research.to_dict())
    return jsonify({'message': 'Research title not found'}), 404


# POST: create
@app.route('/api/researchtitles', methods=['POST'])
def create_research_title():
    data, err = read_body()
    if err:
        return err
    research = Research(**{f: data[f] for f in FIELDS})
    db.session.add(research)
    db.session.commit()
    return jsonify(research.to_dict()), 201


# PUT: update
@app.route('/api/researchtitles/<int:id>', methods=['PUT'])
def update_research_title(id):
    research = db.session.get(Research, id)
    if not research:
        return jsonify({'message': 'Research title not found'}), 404
    data, err = read_body()
    if err:
        return err
    for f in FIELDS:
        setattr(research, f, data[f])
    db.session.commit()
    return jsonify(research.to_dict())


# DELETE
@app.route('/api/researchtitles/<int:id>', methods=['DELETE'])
def delete_research_title(id):
    research = db.session.get(Research, id)
    if not research:
        return jsonify({'message': 'Research title not found'}), 404
    db.session.delete(research)
    db.session.commit()
    return jsonify({'message': 'Research title deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)