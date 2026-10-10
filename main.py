from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///research_opportunities.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class ResearchOpportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    research_title = db.Column(db.String(200), nullable=False)
    research_description = db.Column(db.Text, nullable=False)
    research_area = db.Column(db.String(100), nullable=False)
    faculty_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    required_skills = db.Column(db.String(300), nullable=False)
    available_positions = db.Column(db.Integer, nullable=False)
    application_deadline = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="Open")

    def to_dict(self):
        return {
            "id": self.id,
            "research_title": self.research_title,
            "research_description": self.research_description,
            "research_area": self.research_area,
            "faculty_name": self.faculty_name,
            "department": self.department,
            "required_skills": self.required_skills,
            "available_positions": self.available_positions,
            "application_deadline": self.application_deadline,
            "status": self.status
        }


with app.app_context():
    db.create_all()


def validate_opportunity(data, is_update=False):
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    required_fields = [
        "research_title",
        "research_description",
        "research_area",
        "faculty_name",
        "department",
        "required_skills",
        "available_positions",
        "application_deadline"
    ]

    if not is_update:
        for field in required_fields:
            if field not in data:
                return field + " is required"

    string_fields = [
        "research_title",
        "research_description",
        "research_area",
        "faculty_name",
        "department",
        "required_skills",
        "application_deadline"
    ]

    for field in string_fields:
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                return field + " must be a non-empty string"

    if "available_positions" in data:
        positions = data["available_positions"]

        if type(positions) is not int or positions < 1:
            return "available_positions must be a positive integer"

    if "status" in data:
        if data["status"] not in ["Open", "Closed"]:
            return "status must be Open or Closed"

    if "application_deadline" in data:
        try:
            date.fromisoformat(data["application_deadline"])
        except ValueError:
            return "application_deadline must use YYYY-MM-DD format"

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Research Opportunity Portal API is running"
    }), 200


@app.route("/api/opportunities", methods=["POST"])
def create_opportunity():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "A valid JSON body is required"}), 400

    error = validate_opportunity(data)

    if error:
        return jsonify({"error": error}), 400

    opportunity = ResearchOpportunity(
        research_title=data["research_title"].strip(),
        research_description=data["research_description"].strip(),
        research_area=data["research_area"].strip(),
        faculty_name=data["faculty_name"].strip(),
        department=data["department"].strip(),
        required_skills=data["required_skills"].strip(),
        available_positions=data["available_positions"],
        application_deadline=data["application_deadline"],
        status=data.get("status", "Open")
    )

    db.session.add(opportunity)
    db.session.commit()

    return jsonify(opportunity.to_dict()), 201


@app.route("/api/opportunities", methods=["GET"])
def get_opportunities():
    opportunities = ResearchOpportunity.query.all()

    return jsonify([
        opportunity.to_dict() for opportunity in opportunities
    ]), 200


@app.route("/api/opportunities/<int:opportunity_id>", methods=["GET"])
def get_opportunity(opportunity_id):
    opportunity = db.session.get(ResearchOpportunity, opportunity_id)

    if opportunity is None:
        return jsonify({"error": "Research opportunity not found"}), 404

    return jsonify(opportunity.to_dict()), 200


@app.route("/api/opportunities/<int:opportunity_id>", methods=["PUT"])
def update_opportunity(opportunity_id):
    opportunity = db.session.get(ResearchOpportunity, opportunity_id)

    if opportunity is None:
        return jsonify({"error": "Research opportunity not found"}), 404

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "A valid JSON body is required"}), 400

    error = validate_opportunity(data, is_update=True)

    if error:
        return jsonify({"error": error}), 400

    allowed_fields = [
        "research_title",
        "research_description",
        "research_area",
        "faculty_name",
        "department",
        "required_skills",
        "available_positions",
        "application_deadline",
        "status"
    ]

    for field in allowed_fields:
        if field in data:
            value = data[field]

            if isinstance(value, str):
                value = value.strip()

            setattr(opportunity, field, value)

    db.session.commit()

    return jsonify(opportunity.to_dict()), 200


@app.route("/api/opportunities/<int:opportunity_id>", methods=["DELETE"])
def delete_opportunity(opportunity_id):
    opportunity = db.session.get(ResearchOpportunity, opportunity_id)

    if opportunity is None:
        return jsonify({"error": "Research opportunity not found"}), 404

    db.session.delete(opportunity)
    db.session.commit()

    return jsonify({
        "message": "Research opportunity deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)