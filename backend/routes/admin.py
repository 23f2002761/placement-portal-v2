from flask import Blueprint, request, jsonify
from extensions import db
from models.models import User, Student, Company, JobPosition, Application
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

# 1. Dashboard stats
@admin_bp.route('/admin/dashboard', methods=['GET'])
@admin_required
def dashboard():
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = JobPosition.query.count()
    total_applications = Application.query.count()

    companies = Company.query.all()

    company_list = []
    for company in companies:
        company_list.append({
            "id": company.id,
            "company_name": company.company_name,
            "email": company.user.email,
            "industry": company.industry,
            "location": company.location,
            "is_approved": company.user.is_approved
        })

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "companies": company_list
    })

# 2. Approve Company
@admin_bp.route('/admin/approve-company/<int:company_id>', methods=['PUT'])
@admin_required
def approve_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    company.user.is_approved = True
    db.session.commit()

    return jsonify({"message": "Company approved"})


# 3. Remove Company
@admin_bp.route('/admin/remove-company/<int:company_id>', methods=['DELETE'])
@admin_required
def remove_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    db.session.delete(company)
    db.session.commit()

    return jsonify({"message": "Company removed"})


# 4. Approve Job
@admin_bp.route('/admin/job/<int:job_id>/status', methods=['PUT'])
@admin_required
def update_job_status(job_id):
    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({"message": "Job not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    # only admin-controlled states
    allowed = ["approved", "rejected"]

    if new_status not in allowed:
        return jsonify({"error": "Invalid status"}), 400

    # prevent re-approving or re-rejecting
    if job.status != "pending":
        return jsonify({"error": "Job already reviewed"}), 400

    job.status = new_status
    db.session.commit()

    return jsonify({"message": f"Job {new_status} successfully"})


# 5. Remove Job
@admin_bp.route('/admin/remove-job/<int:job_id>', methods=['DELETE'])
@admin_required
def remove_job(job_id):
    job = JobPosition.query.get(job_id)
    if not job:
        return jsonify({"message": "Job not found"}), 404

    db.session.delete(job)
    db.session.commit()

    return jsonify({"message": "Job removed"})


# 6. Search Companies
@admin_bp.route('/admin/search/companies', methods=['GET'])
@admin_required
def search_companies():
    query = request.args.get('q', '')

    companies = Company.query.filter(
        (Company.company_name.ilike(f"%{query}%")) |
        (Company.industry.ilike(f"%{query}%"))
    ).all()

    result = []
    for c in companies:
        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "industry": c.industry
        })

    return jsonify(result)


# 7. Search Students
@admin_bp.route('/admin/search/students', methods=['GET'])
@admin_required
def search_students():
    query = request.args.get('q', '')

    students = Student.query.join(User).filter(
        (Student.name.ilike(f"%{query}%")) |
        (User.email.ilike(f"%{query}%")) |
        (Student.phone.ilike(f"%{query}%")) |
        (Student.id == query if query.isdigit() else False)
    ).all()

    result = []
    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.user.email,
            "phone":s.phone
        })

    return jsonify(result)


# 8. Deactivate User
@admin_bp.route('/admin/deactivate-user/<int:user_id>', methods=['PUT'])
@admin_required
def deactivate_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.role == "student":
        user.is_active = False

    elif user.role == "company":
        company = Company.query.filter_by(user_id=user.id).first()
        if company:
            company.is_blacklisted = True
        user.is_active = False

    db.session.commit()

    return jsonify({"message": "User updated successfully"})

# 9. Job list
@admin_bp.route('/admin/jobs', methods=['GET'])
@admin_required
def get_all_jobs():
    jobs = JobPosition.query.all()

    result = []
    for j in jobs:
        result.append({
            "id": j.id,
            "title": j.title,
            "status": j.status,
            "company_id": j.company_id
        })

    return jsonify(result)

# 10.Application list
@admin_bp.route('/admin/applications', methods=['GET'])
@admin_required
def get_all_applications():
    applications = Application.query.all()

    result = []
    for a in applications:
        result.append({
            "id": a.id,
            "student_id": a.student_id,
            "job_id": a.job_id,
            "status": a.status
        })

    return jsonify(result)