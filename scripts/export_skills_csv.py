from __future__ import annotations

from pathlib import Path
from datetime import datetime
import pandas as pd

from app.db import engine


def export_skills_csv(output_dir: str = "output", top_n: int = 50) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    query = f"""
    SELECT s.name AS skill, COUNT(*) AS count
    FROM job_skills js
    JOIN skills s ON s.id = js.skill_id
    GROUP BY s.name
    ORDER BY count DESC
    LIMIT {top_n};
    """

    df = pd.read_sql(query, engine)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"skills_summary_{ts}.csv"
    df.to_csv(out_path, index=False)

    print(f"Saved CSV: {out_path} (rows={len(df)})")
    return out_path


if __name__ == "__main__":
    export_skills_csv()
