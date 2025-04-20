from typing import List
from fastapi import FastAPI
from fastapi.routing import APIRouter
from mangum import Mangum
from dotenv import load_dotenv
import uvicorn

from app.models.jobpost import JobPost
from app.models.analysisresults import AnalysisResults
from app.models.jobpost_request import JobPostRequest

#from app.services.indeedlookupservice import IndeedLookupService
from app.services.freelancerservice import FreelancerService
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import random
import numpy as np

# Load environment variables from .env file
load_dotenv()

api_router = APIRouter()


@api_router.get("/health")
def read_root():
    return {"Heathcheck": "OK"}

@api_router.post("/evaluatejobpost", response_model=AnalysisResults)
def eval_jobpost(job: JobPost):
    
    #TODO: Implement the logic to evaluate the job post and return the analysis results.
    print(f"Evaluating job post: {job}")
    isrealFactor = random.randint(1, 100)
    isreal = (isrealFactor % 2 == 0)
    print(f"Is the job post real? {isreal}")
    results = AnalysisResults()
    
    results.is_real = isreal
    results.job_post = job
    return results
    
    
    

@api_router.post("/getjobpost", response_model=JobPost|None)
def get_jobpost(request: JobPostRequest):
    """
    Get job post info from an indeed job post url.
    """
    # Example URL: https://www.indeed.com/viewjob?jk=1234567890abcdefg
    url = request.url
    service = FreelancerService()
    job = service.get_job(url)
    
    
    # Convert the Pydantic model to a JSON-serializable format
    if( job is None):
        return JSONResponse(status_code=404, content={"message": "Job post not found."})
    job_json = jsonable_encoder(job)
    
    return JSONResponse(content=job_json)


app = FastAPI()
app.include_router(api_router, prefix='/api')  # Include your router here

# This is the entry point for the AWS Lambda function.
handler = Mangum(app)

# The following code is for local testing. It will not be executed in AWS Lambda.

if __name__ == '__main__':
    uvicorn.run('main:app', port=3000)