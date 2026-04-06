from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        password_hash=hashed_password,
        role='student',
        is_approved=True
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Student registered successfully"}), 201

@auth_bp.route('/register/company', methods=['POST'])
def register_company():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        password_hash=hashed_password,
        role='company',
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Company registered. Awaiting approval"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not present"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Incorrect Password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    if user.role == 'company':
        if not user.is_approved:
            return jsonify({"error": "Company not approved"}), 403

    access_token = create_access_token(
    identity=str(user.id),
    additional_claims={
        "role": user.role,
        "email": user.email
    }
)

    return jsonify({
        "access_token": access_token
    }), 200
