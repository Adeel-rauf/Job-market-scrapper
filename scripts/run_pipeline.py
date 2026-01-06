from scripts.export_skills_csv import export_skills_csv
import os

def main():
    # GitHub Actions runner: NO Selenium scraping
    if os.getenv("GITHUB_ACTIONS") == "true":
            from scripts.export_skills_csv_ci import main as export_ci
            export_ci()
            return



    # Local run: scrape + save to DB, then export CSV
    from app.scrapers.remote import run as run_remote
    run_remote()

    from scripts.export_skills_csv import export_skills_csv
    export_skills_csv()

if __name__ == "__main__":
    main()
