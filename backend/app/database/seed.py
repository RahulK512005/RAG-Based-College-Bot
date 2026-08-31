import os
import sys
import glob

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import UploadFile
from app.database.session import SessionLocal, init_db
from app.models.user import User
from app.models.document import Document
from app.core.security import hash_password
from app.services.document_service import document_service

SAMPLE_DOCS_METADATA = {
    "Admissions_Handbook_2026.txt": {
        "title": "Admissions Handbook 2026",
        "category": "Admissions",
        "department": "Undergraduate Admissions",
        "academic_year": "2026-2027",
        "description": "Official guide on eligibility, cutoffs, seat distribution, and counseling dates."
    },
    "Fee_Structure_2026.txt": {
        "title": "Academic Fee Structure 2026",
        "category": "Fees",
        "department": "Finance & Accounts",
        "academic_year": "2026-2027",
        "description": "Complete breakdown of tuition, lab fees, one-time deposits, and refund rules."
    },
    "Academic_Calendar_2026.txt": {
        "title": "Official Academic Calendar 2026",
        "category": "Academics",
        "department": "Dean Academics",
        "academic_year": "2026-2027",
        "description": "Fall and Spring semester timelines, mid-terms, final exams, and fests."
    },
    "Hostel_Rules_and_Facilities.txt": {
        "title": "Hostel Residence Manual & Rules",
        "category": "Hostel",
        "department": "Student Housing",
        "academic_year": "2026-2027",
        "description": "Room sharing options, curfew times, mess fees, and code of conduct."
    },
    "Placements_and_Career_Services.txt": {
        "title": "Placement & Career Development Report",
        "category": "Placements",
        "department": "Career Development Cell",
        "academic_year": "2025-2026",
        "description": "Top recruiters, salary packages, dream company policy, and internship guidelines."
    },
    "Scholarships_and_Financial_Aid.txt": {
        "title": "Scholarship & Financial Aid Schemes",
        "category": "Scholarships",
        "department": "Student Welfare",
        "academic_year": "2026-2027",
        "description": "Merit waivers, need-based EWS support, women in tech fellowships, and sports quotas."
    }
}

def seed_database():
    print("[INIT] Initializing Database Schema...")
    init_db()
    db = SessionLocal()

    try:
        # 1. Seed Admin User
        admin = db.query(User).filter(User.email == "admin@college.edu").first()
        if not admin:
            admin = User(
                name="College Administrator",
                email="admin@college.edu",
                password_hash=hash_password("Admin@123456"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("[SUCCESS] Admin user created: admin@college.edu / Admin@123456")
        else:
            print("[INFO] Admin user already exists.")

        # 2. Seed Demo Student User
        student = db.query(User).filter(User.email == "student@college.edu").first()
        if not student:
            student = User(
                name="Alex Sharma",
                email="student@college.edu",
                password_hash=hash_password("Student@123456"),
                role="student"
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            print("[SUCCESS] Demo student created: student@college.edu / Student@123456")
        else:
            print("[INFO] Demo student user already exists.")

        # 3. Ingest Sample Documents into Vector Store
        sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../sample_documents"))
        if not os.path.exists(sample_dir):
            sample_dir = os.path.abspath("sample_documents")

        doc_files = glob.glob(os.path.join(sample_dir, "*.txt"))
        print(f"[INFO] Found {len(doc_files)} sample knowledge documents in {sample_dir}.")

        for file_path in doc_files:
            fname = os.path.basename(file_path)
            meta = SAMPLE_DOCS_METADATA.get(fname, {
                "title": fname.replace(".txt", "").replace("_", " "),
                "category": "General",
                "department": "Administration",
                "academic_year": "2026",
                "description": "College information document."
            })

            # Check if document already exists
            existing_doc = db.query(Document).filter(Document.title == meta["title"]).first()
            if not existing_doc:
                print(f"[INGEST] Ingesting & embedding: {meta['title']}...")
                with open(file_path, "rb") as f:
                    upload_file = UploadFile(filename=fname, file=f)
                    doc = document_service.upload_and_process(
                        db=db,
                        file=upload_file,
                        title=meta["title"],
                        category=meta["category"],
                        department=meta["department"],
                        academic_year=meta["academic_year"],
                        description=meta["description"],
                        user_id=admin.id
                    )
                    print(f"   -> Status: {doc.processing_status} | ID: {doc.id}")
            else:
                print(f"[INFO] Document '{meta['title']}' already indexed (Status: {existing_doc.processing_status}).")

        print("[COMPLETE] Database seeding and vector ingestion complete!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
