from pydantic import BaseModel
from decimal import Decimal

class JobPost(BaseModel):
    title: str = ''
    #description = company_profile + requirements + required_experience + required_education + industry + function + title + location
    description: str = ''
    requirements: str = ''