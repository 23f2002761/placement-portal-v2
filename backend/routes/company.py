from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.models import User, Student, Company, JobPosition, Application
from datetime import datetime
from utils.decorators import company_required

company_bp = Blueprint('company', __name__)


# ✅ Helper
def get_current_company():
    user_id = get_jwt_identity()  

    if not user_id:
        return None

    return Company.query.filter_by(user_id=user_id).first()


# ✅ 1. Dashboard
@company_bp.route('/company/dashboard', methods=['GET'])
@jwt_required()
@company_required
def dashboard():
    company = get_current_company()

    if not company or not company.user.is_approved:
        return jsonify({"error": "Company not approved"}), 403

    total_jobs = JobPosition.query.filter_by(company_id=company.id).count()

    total_applications = db.session.query(Application)\
        .join(JobPosition)\
        .filter(JobPosition.company_id == company.id)\
        .count()

    shortlisted_count = db.session.query(Application)\
        .join(JobPosition)\
        .filter(
            JobPosition.company_id == company.id,
            Application.status == "shortlisted"
        ).count()

    jobs = JobPosition.query.filter_by(company_id=company.id).all()

    job_list = []
    for job in jobs:

        # count applicants per job (optional but useful)
        applicant_count = Application.query.filter_by(job_id=job.id).count()

        job_list.append({
            "id": job.id,
            "title": job.title,
            "skills": job.skills,
            "salary": job.salary,
            "status": job.status,
            "created_at": job.created_at.strftime("%Y-%m-%d") if job.created_at else None,
            "applicant_count": applicant_count ,
            "status":job.status  # ✅ useful for UI
        })


    return jsonify({
        "company": {
            "id": company.id,
            "name": company.company_name,
            "industry": company.industry
        },
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "shortlisted_candidates": shortlisted_count,
        "jobs": job_list
    })


# ✅ 2. Create Job (FULL)
@company_bp.route('/company/create-job', methods=['POST'])
@jwt_required()
@company_required
def create_job():
    company = get_current_company()

    if not company or not company.user.is_approved:
        return jsonify({"error": "Company not approved"}), 403

    data = request.get_json() or {}

    deadline_str = data.get('deadline')
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d") if deadline_str else None

    job = JobPosition(
        company_id=company.id,
        title=data.get('title'),
        description=data.get('description'),
        salary=data.get('salary'),
        eligibility_branch=data.get('eligibility_branch'),
        eligibility_cgpa=data.get('eligibility_cgpa'),
        deadline=deadline,
        skills=data.get('skills'),
        experience=data.get('experience'),
        benefits=data.get('benefits'),
        status="pending"
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({"message": "Job created, pending admin approval"}), 201



# ✅ 3. Get Applicants
@company_bp.route('/company/job/<int:job_id>/applications', methods=['GET'])
@jwt_required()
@company_required
def get_applications(job_id):
    company = get_current_company()

    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first()

    if not job:
        return jsonify({"error": "Unauthorized or job not found"}), 404
    
    if job.status != "approved":
        return jsonify({"error": "Job not active"}), 400

    applications = Application.query.filter_by(job_id=job_id).all()

    result = []
    for app in applications:
        student = Student.query.filter_by(id=app.student_id).first()
        if not student:
            continue

        result.append({
            "application_id": app.id,
            "status": app.status,
            "feedback": app.feedback,
            "interview_date": str(app.interview_date) if app.interview_date else None,
            "student": {
                "name": student.name,
                "branch": student.branch,
                "cgpa": student.cgpa
            }
        })

    return jsonify(result)


# ✅ 4. Update Application Status + Feedback
@company_bp.route('/company/application/<int:app_id>/status', methods=['PUT'])
@jwt_required()
@company_required
def update_application_status(app_id):
    company = get_current_company()

    app = Application.query.get(app_id)

    if not app:
        return jsonify({"error": "Application not found"}), 404

    job = JobPosition.query.get(app.job_id)

    if job.company_id != company.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    if job.status != "approved":
        return jsonify({"error": "Job not active"}), 400

    data = request.get_json() or {}
    new_status = data.get("status")
    feedback = data.get("feedback")

    allowed = ["shortlisted", "interview", "selected", "rejected"]

    if new_status not in allowed:
        return jsonify({"error": "Invalid status"}), 400

    valid_transitions = {
        "applied": ["shortlisted", "rejected"],
        "shortlisted": ["interview", "rejected"],
        "interview": ["selected", "rejected"],
        "selected": [],
        "rejected": []
    }

    current_status = app.status

    if new_status not in valid_transitions.get(current_status, []):
        return jsonify({
            "error": f"Cannot move from {current_status} to {new_status}"
        }), 400

    app.status = new_status
    app.feedback = feedback

    db.session.commit()

    return jsonify({"message": "Application updated successfully"})

# ✅ 5. Close Job
@company_bp.route('/company/job/<int:job_id>/close', methods=['PUT'])
@jwt_required()
@company_required
def close_job(job_id):
    company = get_current_company()

    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first()

    if not job:
        return jsonify({"error": "Unauthorized or job not found"}), 404

    if job.status != "approved":
        return jsonify({"error": "Only approved jobs can be closed"}), 400

    job.status = "closed"
    db.session.commit()

    return jsonify({"message": "Job closed successfully"})

# ✅ 6. Schedule Interview
@company_bp.route('/company/application/<int:app_id>/schedule', methods=['PUT'])
@jwt_required()
@company_required
def schedule_interview(app_id):
    company = get_current_company()

    app = Application.query.get(app_id)

    if not app:
        return jsonify({"error": "Application not found"}), 404

    job = JobPosition.query.get(app.job_id)

    if job.company_id != company.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    if job.status != "approved":
        return jsonify({"error": "Job not active"}), 400

    data = request.get_json() or {}

    if app.status != "shortlisted":
        return jsonify({"error": "Only shortlisted candidates can be scheduled"}), 400

    app.interview_date = data.get("interview_date")
    app.interview_location = data.get("interview_location")
    app.status = "interview"
    db.session.commit()

    return jsonify({"message": "Interview scheduled"})

