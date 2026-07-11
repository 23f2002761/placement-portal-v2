from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp
from flask_cors import CORS
from flask_mail import Message
# from flask_mail import Mail
# from utils.decorators import admin_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ash769980@gmail.com'
app.config['MAIL_PASSWORD'] = 'qfxdfndzuqqwwotg'
app.config['MAIL_DEFAULT_SENDER'] = 'ash769980@gmail.com'

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

from extensions import db, jwt , mail ,cache


db.init_app(app)
jwt.init_app(app)
mail.init_app(app)
cache.init_app(app)

CORS(app) 

from models.models import User, Student, Company, JobPosition, Application, Placement

from routes.auth import auth_bp
 

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(company_bp, url_prefix='/api')
app.register_blueprint(student_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Placement Portal Backend Running"

@app.route('/test-email')
def test_email():
    msg = Message(
        subject="Placement Portal Test",
        recipients=["ash769980@gmail.com"]   
    )

    msg.body = "This is a test email from your Placement Portal."

    mail.send(msg)

    return "Test email sent successfully!"

# @app.route('/admin-test')
# @admin_required
# def admin_test():
#     return {"message": "Admin access granted"}


if __name__ == '__main__':
    app.run(debug=True)
