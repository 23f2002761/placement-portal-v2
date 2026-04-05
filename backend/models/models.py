from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    company = db.relationship('Company', backref='user', uselist=False)
    student = db.relationship('Student', backref='user', uselist=False)

    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.Text)
    phone = db.Column(db.String(15))
    branch = db.Column(db.String(50))
    resume_path = db.Column(db.String(255))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)

    placements = db.relationship('Placement', backref='student')
    applications = db.relationship('Application', backref='student', cascade="all, delete-orphan")

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    location = db.Column(db.String(100))
    company_name = db.Column(db.String(150), nullable=False)
    industry = db.Column(db.String(100))
    website = db.Column(db.String(150))
    is_blacklisted = db.Column(db.Boolean, default=False)

    job_positions = db.relationship('JobPosition', backref='company', cascade="all, delete-orphan")
    placements = db.relationship('Placement', backref='company')

    hr_contact = db.Column(db.String(100))

class JobPosition(db.Model):
    __tablename__ = 'job_positions'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    salary = db.Column(db.Float)
    eligibility_cgpa = db.Column(db.Float)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="open")

    applications = db.relationship('Application', backref='job', cascade="all, delete-orphan")
    placements = db.relationship('Placement', backref='job')

    eligibility_branch = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    __tablename__ = 'applications'
    __table_args__ = (
        db.UniqueConstraint('student_id', 'job_id', name='unique_student_job'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_positions.id'), nullable=False)
    status = db.Column(db.String(50), default="applied")
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

class Placement(db.Model):
    __tablename__ = 'placements'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_positions.id'), nullable=False)
    salary = db.Column(db.Float)
    joining_date = db.Column(db.DateTime)
