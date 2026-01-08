# Job Market Intelligence Scraper 🚀

A production-style **job market data pipeline** that scrapes RemoteOK, stores structured job data in PostgreSQL, extracts in-demand skills, and exports clean CSV reports for analysis and dashboards.

This project demonstrates **end-to-end data engineering**: scraping, persistence, transformation, analytics, and automation.

---

## 🔧 Tech Stack

- **Python 3.12**
- **Selenium + BeautifulSoup** (dynamic scraping)
- **PostgreSQL**
- **SQLAlchemy 2.0 + Alembic**
- **Pandas**
- **GitHub Actions (scheduled automation)**

---

## 📌 What This Project Does

### 1️⃣ Scrapes Jobs (RemoteOK)
- Job title
- Company
- Location
- Job URL
- Full job description
- Posted & scraped timestamps

### 2️⃣ Stores Data Reliably
- Normalized relational schema
- `jobs`, `companies`, `skills`, `job_skill`
- Duplicate-safe inserts

### 3️⃣ Extracts Skill Intelligence
- Regex-based skill extraction from job titles & descriptions
- Aggregates skill demand across all jobs

### 4️⃣ Exports Analytics-Ready CSVs
- **Skills summary CSV** (market trends)
- **Jobs export CSV** (full listings)

### 5️⃣ Runs Automatically
- GitHub Actions workflow (daily or manual)
- CI-safe execution without database secrets

---

## 📂 Project Structure

```text
job-market-scraper/
├── app/
│   ├── scrapers/        # RemoteOK scraper
│   ├── models/          # SQLAlchemy models
│   ├── repository.py   # DB operations
│   └── db.py
├── scripts/
│   ├── run_pipeline.py
│   ├── export_jobs_csv.py
│   ├── export_skills_csv.py
│   └── backfill_skills.py
├── alembic/             # DB migrations
├── data/                # Sample CSVs
├── .github/workflows/   # CI automation
└── README.md
