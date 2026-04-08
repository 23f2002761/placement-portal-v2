from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime
from routes.admin import admin_bp
from routes.company import company_bp
# from utils.decorators import admin_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

from extensions import db, jwt

db.init_app(app)
jwt.init_app(app)

from models.models import User, Student, Company, JobPosition, Application, Placement

from routes.auth import auth_bp

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(company_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Placement Portal Backend Running"

# @app.route('/admin-test')
# @admin_required
# def admin_test():
#     return {"message": "Admin access granted"}

if __name__ == '__main__':
    app.run(debug=True)
