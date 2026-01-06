import os

def main():
    # GitHub Actions runner: NO Selenium scraping
    if os.getenv("GITHUB_ACTIONS") == "true":
        # Export from DB if available; otherwise create a clear message file.
        try:
            from scripts.export_skills_csv import export_skills_csv
            export_skills_csv()
        except Exception as e:
            from pathlib import Path
            from datetime import datetime

            Path("output").mkdir(exist_ok=True)
            ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            p = Path("output") / f"ci_note_{ts}.txt"
            p.write_text(
                "CI run completed, but database was not available to export skills.\n"
                f"Error: {e}\n",
                encoding="utf-8",
            )
            print("CI finished (no DB available).")
        return

    # Local run: scrape + save to DB, then export CSV
    from app.scrapers.remote import run as run_remote
    run_remote()

    from scripts.export_skills_csv import export_skills_csv
    export_skills_csv()

if __name__ == "__main__":
    main()
