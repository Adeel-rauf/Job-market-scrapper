from app.models.skills import extract_skills_from_fields
from app.repository import upsert_skill, link_job_skill
from sqlalchemy import select
from app.db import SessionLocal
from app.models.job import Job

def main(limit: int = 5000):
    total_links = 0
    with SessionLocal() as session:
        jobs = session.execute(select(Job).limit(limit)).scalars().all()

        for job in jobs:
            skills = extract_skills_from_fields(job.title, job.description)
            for s in skills:
                skill_id = upsert_skill(session, s)
                link_job_skill(session, job.id, skill_id)
                total_links += 1

        session.commit()

    print(f"Processed jobs={len(jobs)}; created links={total_links}")

if __name__ == "__main__":
    main()
