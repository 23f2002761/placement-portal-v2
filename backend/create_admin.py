from app import app, db
from models.models import User
from werkzeug.security import generate_password_hash

with app.app_context():

    existing_admin = User.query.filter_by(email="admin@ppa.com").first()

    if not existing_admin:
        admin = User(
            email="admin@ppa.com",
            password_hash=generate_password_hash("admin123"),
            role="admin",
            is_active=True,
            is_approved=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully")
    else:
        print("Admin already exists")
