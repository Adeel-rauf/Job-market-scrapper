from __future__ import annotations

import pandas as pd
from pathlib import Path
from datetime import datetime

from app.scrapers.remote import run as run_remote  # adjust if your file name differs

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    # Run scraper (will insert into DB locally if DB exists, but in Actions we just want the scrape)
    # We'll modify the scraper to also RETURN data next step. For now we just run it.
    run_remote()

    # Placeholder CSV (we’ll make it real in next step)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out = OUTPUT_DIR / f"run_{ts}.txt"
    out.write_text("Run completed\n", encoding="utf-8")
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()
