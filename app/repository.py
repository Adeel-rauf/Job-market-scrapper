from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.company import Company
from app.models.job import Job
from app.models.skills import Skill
from app.models.job_skill import JobSkill
from sqlalchemy.dialects.postgresql import insert


def get_or_create_company(session: Session, name: str, location: str | None = None) -> Company:
    name = name.strip()
    existing = session.execute(select(Company).where(Company.name == name)).scalar_one_or_none()
    if existing:
        return existing

    company = Company(name=name, location=location)
    session.add(company)
    session.flush()
    return company


def upsert_job(
    session: Session,
    *,
    title: str,
    location: str,
    company: Company,
    url: str,
    description: str | None = None,
) -> bool:
    """
    True if inserted, False if already existed.
    """
    stmt = insert(Job).values(
        title=title,
        location=location,
        company_id=company.id,
        url=url.strip(),
        description=description,
    ).on_conflict_do_nothing(
        index_elements=[Job.url]  
    )

    result = session.execute(stmt)
    
    return result.rowcount == 1

def upsert_skill(session: Session, name: str) -> int:
    """
    Returns skill_id
    """
    name = name.strip().lower()

    stmt = insert(Skill).values(name=name).on_conflict_do_update(
        index_elements=[Skill.name],
        set_={"name": name},
    ).returning(Skill.id)

    skill_id = session.execute(stmt).scalar_one()
    return skill_id


def link_job_skill(session: Session, job_id: int, skill_id: int) -> None:
    stmt = insert(JobSkill).values(job_id=job_id, skill_id=skill_id).on_conflict_do_nothing(
        constraint="uq_job_skill"
    )
    session.execute(stmt)
