from pydantic import BaseModel
from app.models.jobpost import JobPost

class AnalysisResults(BaseModel):
    job_post: JobPost = JobPost()
    is_real: bool = False    