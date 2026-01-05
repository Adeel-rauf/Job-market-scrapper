from pydantic import BaseModel, HttpUrl, Field

class JobSkillExtractionIn(BaseModel):
    job_id: int = Field(gt=0)
    url: HttpUrl
