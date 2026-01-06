import os

def main() -> None:
    # CI mode: DO NOT import app.db or SQLAlchemy at all
    if os.getenv("GITHUB_ACTIONS") == "true":
        from scripts.export_skills_csv_ci import main as export_ci
        export_ci()
        return

    # Local mode: full pipeline (DB + scraper + export)
    from app.scrapers.remote import run as run_remote
    run_remote()

    from scripts.export_skills_csv import export_skills_csv
    export_skills_csv()

if __name__ == "__main__":
    main()
