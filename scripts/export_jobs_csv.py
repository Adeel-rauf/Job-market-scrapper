import pandas as pd
from app.db import engine

query = """
SELECT
  j.title,
  c.name AS company,
  j.location,
  j.url,
  j.posted_at
FROM jobs j
LEFT JOIN companies c ON c.id = j.company_id
ORDER BY j.scraped_at DESC
"""

df = pd.read_sql(query, engine)
df.to_csv("jobs_export.csv", index=False)

print(f"Exported {len(df)} jobs")
