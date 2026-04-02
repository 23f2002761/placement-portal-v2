from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models.models import User, Student, Company, JobPosition, Application, Placement

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Placement Portal Backend Running"

if __name__ =='__main__':
    app.run(debug=True)
