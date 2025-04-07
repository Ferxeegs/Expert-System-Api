from flask import Blueprint, request, jsonify
from app.inference import diagnose_disease

bp = Blueprint('api', __name__)

@bp.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    symptoms = set(data.get("symptoms", []))
    
    result = diagnose_disease(symptoms)
    return jsonify(result)
