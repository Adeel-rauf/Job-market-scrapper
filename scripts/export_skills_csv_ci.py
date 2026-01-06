from __future__ import annotations

from pathlib import Path
import shutil


def main() -> None:
    """
    CI-safe exporter:
    - Does NOT require DATABASE_URL
    - Copies data/sample_skills.csv -> output/skills_summary.csv
    """
    src = Path("data") / "sample_skills.csv"
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    dst = out_dir / "skills_summary.csv"

    if not src.exists():
        # Always produce something so the workflow has an artifact
        dst.write_text("skill,count\n", encoding="utf-8")
        print("sample_skills.csv not found, wrote empty skills_summary.csv")
        return

    shutil.copyfile(src, dst)
    print(f"CI export created: {dst}")


if __name__ == "__main__":
    main()
