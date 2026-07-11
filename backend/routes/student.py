from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db ,cache
from models.models import Student, User, JobPosition, Application, Company,Placement
from utils.decorators import student_required
from flask import send_file
# from tasks.export_tasks import export_student_applications
import os

student_bp = Blueprint('student', __name__)


# ✅ Helper
def get_current_student():
    user_id = get_jwt_identity()

    if not user_id:
        return None

    return Student.query.filter_by(user_id=int(user_id)).first()


# ✅ 1. Dashboard
@student_bp.route('/student/dashboard', methods=['GET'])
@jwt_required()
@student_required
def dashboard():
    student = get_current_student()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Total applications
    applications_query = Application.query.filter_by(student_id=student.id)

    total_applications = applications_query.count()

    # Fetch application list
    applications = applications_query.all()

    application_list = []
    for app in applications:
        application_list.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": app.job.title if app.job else None,
            "company_name": app.job.company.company_name if app.job and app.job.company else None,
            "status": app.status,
            "applied_at": app.created_at.strftime("%Y-%m-%d") if app.created_at else None
        })

    return jsonify({
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.user.email,
            "phone": student.phone,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "year": student.year,
            "skills": student.skills,
            "resume": student.resume_path
        },
        "total_applications": total_applications,
        "applications": application_list
    })


# ✅ 2. Update Profile
@student_bp.route('/student/profile', methods=['PUT'])
@jwt_required()
@student_required
def update_profile():
    student = get_current_student()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json() or {}

    student.name = data.get("name", student.name)
    student.phone = data.get("phone", student.phone)
    student.branch = data.get("branch", student.branch)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.year = data.get("year", student.year)
    student.skills = data.get("skills", student.skills)
    student.education = data.get("education", student.education)
    student.experience = data.get("experience", student.experience)
    student.resume_path = data.get("resume_path", student.resume_path)

    db.session.commit()
    cache.clear()

    return jsonify({"message": "Profile updated successfully"})


# ✅ 3. Get Approved Jobs
@student_bp.route('/student/jobs', methods=['GET'])
@jwt_required()
@student_required
@cache.cached(timeout=300)
def get_jobs():
    jobs = JobPosition.query.filter_by(status="approved").all()

    result = []
    for job in jobs:
        result.append({
            "id": job.id,
            "title": job.title,
            "company_name": job.company.company_name,
            "skills": job.skills,
            "salary": job.salary,
            "deadline": job.deadline.strftime("%Y-%m-%d") if job.deadline else None
        })

    return jsonify(result)


# ✅ 4. Search Jobs
@student_bp.route('/student/jobs/search', methods=['GET'])
@jwt_required()
@student_required
def search_jobs():
    query = request.args.get('q', '')

    jobs = JobPosition.query.join(Company).filter(
        JobPosition.status == "approved",
        (
            JobPosition.title.ilike(f"%{query}%") |
            JobPosition.skills.ilike(f"%{query}%") |
            Company.company_name.ilike(f"%{query}%")
        )
    ).all()

    result = []
    for job in jobs:
        result.append({
            "id": job.id,
            "title": job.title,
            "company_name": job.company.company_name,
            "skills": job.skills,
            "salary": job.salary
        })

    return jsonify(result)


# ✅ 5. Apply to Job
@student_bp.route('/student/apply/<int:job_id>', methods=['POST'])
@jwt_required()
@student_required
def apply_job(job_id):
    student = get_current_student()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    job = JobPosition.query.get(job_id)

    if not job or job.status != "approved":
        return jsonify({"error": "Job not available"}), 404

    # prevent duplicate
    existing = Application.query.filter_by(
        student_id=student.id,
        job_id=job_id
    ).first()

    if existing:
        return jsonify({"error": "Already applied"}), 400

    application = Application(
        student_id=student.id,
        job_id=job_id
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Applied successfully"}), 201


# ✅ 6. Application Details
@student_bp.route('/student/application/<int:app_id>', methods=['GET'])
@jwt_required()
@student_required
def get_application_detail(app_id):
    student = get_current_student()

    app = Application.query.filter_by(
        id=app_id,
        student_id=student.id
    ).first()

    if not app:
        return jsonify({"error": "Application not found"}), 404

    return jsonify({
        "application_id": app.id,
        "job_title": app.job.title,
        "company_name": app.job.company.company_name,
        "status": app.status,
        "feedback": app.feedback,
        "interview_date": app.interview_date,
        "interview_location": app.interview_location,
        "applied_on": app.applied_on.strftime("%Y-%m-%d") if app.applied_on else None
    })



# ✅ 7. Interview Details
@student_bp.route('/student/interviews', methods=['GET'])
@jwt_required()
@student_required
def get_interviews():
    student = get_current_student()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    applications = Application.query.filter(
        Application.student_id == student.id,
        Application.interview_date != None
    ).all()

    result = []

    for app in applications:
        result.append({
            "application_id": app.id,
            "job_title": app.job.title,
            "company_name": app.job.company.company_name,
            "interview_date": app.interview_date,
            "interview_location": app.interview_location,
            "status": app.status,
            "feedback": app.feedback
        })

    return jsonify(result)


# ✅ 8. Offer letter
@student_bp.route('/student/offer-letter/<int:app_id>', methods=['GET'])
@jwt_required()
@student_required
def download_offer_letter(app_id):
    student = get_current_student()

    app = Application.query.filter_by(
        id=app_id,
        student_id=student.id
    ).first()

    if not app:
        return jsonify({"error": "Application not found"}), 404

    if app.status not in ["selected", "placed"]:
        return jsonify({"error": "Offer not available yet"}), 403

    if not app.offer_letter_path:
        return jsonify({"error": "Offer letter not uploaded"}), 404

    if not os.path.exists(app.offer_letter_path):
        return jsonify({"error": "File missing"}), 404

    return send_file(app.offer_letter_path, as_attachment=True)


# ✅ 9. Placements
@student_bp.route('/student/placements', methods=['GET'])
@jwt_required()
@student_required
def get_placements():
    student = get_current_student()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    placements = Placement.query.filter_by(student_id=student.id).all()

    result = []
    for p in placements:
        result.append({
            "company_name": p.company.company_name,
            "job_title": p.job.title,
            "salary": p.salary,
            "joining_date": p.joining_date.strftime("%Y-%m-%d") if p.joining_date else None
        })

    return jsonify(result)

# ✅ 10.Export Applications CSV
@student_bp.route('/student/export', methods=['POST'])
@jwt_required()
@student_required
def export_csv():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    from tasks.export_tasks import export_student_applications

    export_student_applications.delay(student.id)

    return jsonify({
        "message": "Export Started"
    }), 202

# ✅ 11.Download Exported CSV
@student_bp.route('/student/download-export', methods=['GET'])
@jwt_required()
@student_required
def download_export():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    filename = f"exports/student_{student.id}_applications.csv"

    import os

    if not os.path.exists(filename):
        return jsonify({
            "error": "Export file not found. Please generate the export first."
        }), 404

    return send_file(
        filename,
        as_attachment=True
    )