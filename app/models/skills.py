from __future__ import annotations
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

import re
from typing import Iterable, Set

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)

# Start with a strong “scraping project” list (expand anytime)
SKILL_PATTERNS: dict[str, str] = {
    # Core languages
    "python": r"\bpython\b",
    "java": r"\bjava\b",
    "javascript": r"\bjavascript\b|\bjs\b",
    "typescript": r"\btypescript\b|\bts\b",
    "c#": r"\bc#\b|\bcsharp\b",
    "go": r"\bgo\b|\bgolang\b",
    "php": r"\bphp\b",
    "ruby": r"\bruby\b",
    "rust": r"\brust\b",

    # Databases
    "sql": r"\bsql\b",
    "postgresql": r"\bpostgres(?:ql)?\b",
    "mysql": r"\bmysql\b",
    "sqlite": r"\bsqlite\b",
    "mongodb": r"\bmongo(?:db)?\b",
    "redis": r"\bredis\b",
    "elasticsearch": r"\belastic(?:search)?\b",

    # Backend frameworks
    "fastapi": r"\bfastapi\b",
    "django": r"\bdjango\b",
    "flask": r"\bflask\b",
    "node.js": r"\bnode\.?js\b|\bnode\b",
    "express": r"\bexpress(?:\.js)?\b",
    "nestjs": r"\bnest(?:js)?\b",
    ".net": r"\b\.net\b|\bdotnet\b",
    "spring": r"\bspring\b|\bspring boot\b",

    # Frontend
    "react": r"\breact\b",
    "next.js": r"\bnext\.?js\b|\bnextjs\b",
    "vue": r"\bvue(?:\.js)?\b|\bvuejs\b",
    "angular": r"\bangular\b",
    "svelte": r"\bsvelte\b",
    "html": r"\bhtml\b",
    "css": r"\bcss\b",

    # Data / ML
    "pandas": r"\bpandas\b",
    "numpy": r"\bnumpy\b",
    "scikit-learn": r"\bscikit[-\s]?learn\b|\bsklearn\b",
    "tensorflow": r"\btensorflow\b",
    "pytorch": r"\bpytorch\b",
    "nlp": r"\bnlp\b|\bnatural language processing\b",

    # Scraping / automation
    "selenium": r"\bselenium\b",
    "beautifulsoup": r"\bbeautiful\s*soup\b|\bbs4\b",
    "scrapy": r"\bscrapy\b",
    "playwright": r"\bplaywright\b",

    # DevOps / Cloud
    "git": r"\bgit\b",
    "github": r"\bgithub\b",
    "github actions": r"\bgithub actions\b",
    "docker": r"\bdocker\b",
    "kubernetes": r"\bkubernetes\b|\bk8s\b",
    "linux": r"\blinux\b",
    "aws": r"\baws\b|\bamazon web services\b",
    "azure": r"\bazure\b",
    "gcp": r"\bgcp\b|\bgoogle cloud\b",
    "terraform": r"\bterraform\b",
    "ci/cd": r"\bci\/cd\b|\bcicd\b",

    # Concepts (useful for dashboard categories)
    "backend": r"\bbackend\b",
    "frontend": r"\bfrontend\b",
    "full stack": r"\bfull\s*stack\b",
    "api": r"\bapi\b|\brest\b|\bgraphql\b",
    "microservices": r"\bmicroservices?\b",
}


_compiled = {k: re.compile(v, re.IGNORECASE) for k, v in SKILL_PATTERNS.items()}

def extract_skills(text: str | None) -> set[str]:
    if not text:
        return set()
    found: set[str] = set()
    for skill, rx in _compiled.items():
        if rx.search(text):
            found.add(skill)
    return found

def extract_skills_from_fields(*fields: str | None) -> set[str]:
    combined = " \n ".join([f for f in fields if f])
    return extract_skills(combined)
