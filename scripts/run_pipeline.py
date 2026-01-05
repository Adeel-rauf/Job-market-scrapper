import os
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # Detect GitHub Actions
    if os.getenv("GITHUB_ACTIONS") == "true":
        # CI-safe behavior (no Selenium)
        out = OUTPUT_DIR / f"ci_run_{ts}.txt"
        out.write_text(
            "CI run successful.\n"
            "Selenium scraping is disabled in GitHub Actions.\n"
            "Local runs perform full scraping.\n",
            encoding="utf-8",
        )
        print("CI run completed safely (no Selenium).")
        return

    # Local run (full Selenium)
    from app.scrapers.remote import run
    run()
    print("Local scrape completed.")

if __name__ == "__main__":
    main()
