from app.db import engine, Base
from app.models.company import Company
from app.models.job import Job

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done ✅")
