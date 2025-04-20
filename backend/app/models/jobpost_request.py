from pydantic import BaseModel

class JobPostRequest(BaseModel):
    url: str