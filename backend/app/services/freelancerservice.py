from app.models.jobpost import JobPost
from bs4 import BeautifulSoup
import requests
from decimal import Decimal
import os
import pandas as pd
from json import JSONDecoder
class FreelancerService:

    def __init__(self):
        self.decoder = JSONDecoder()

    def process_job_skills(self, skills):
        """
        Process job skills from the job post.
        """
        if skills:
            skill_list = ''
            df = pd.json_normalize(skills)
            print(f"Skills:\n\n {df}")
            for val in df['name']:
                print(f"Skill: {val}")
                if len(skill_list) > 0:
                    skill_list += ', '
                skill_list += val
            return skill_list

        return ''

    def get_job(self, url: str):
        """
        Get job info from a SimplyHired job post url.
        """
        # Example URL: https://www.freelancer.com/projects/artificial-intelligence/windows-noise-gate-software-for
        proj = url.split('/projects/')[1]
        print(f"Fetching SimplyHired job post from URL: {url}")
        soup = None
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            json_data = soup.find('script', {"id": "webapp-state"})            
            if json_data:
                json_data = self.decoder.decode(json_data.text)
                #print(f"JSON data: {json_data['NGRX_STATE']['projectsSeo']['0']['documents'][proj]}")
                df = pd.json_normalize(json_data['NGRX_STATE']['projectsSeo']['0']['documents'][proj]) 
                job = JobPost ()
                job.title = df['rawDocument.title'].values[0]
                job.requirements = self.process_job_skills(df['rawDocument.skills'].values[0])
                job.description = f"{df['rawDocument.description'].values[0]}, Skills: {job.requirements}"
                
                print(job)
                df.to_csv('./job_post.csv', index=False)               
                print(f"df info: {df.info()}")
                # Extracting job details from the JSON data
                return job
            else:
                print("No JSON data found in the page.")
                return None            
        else:
            print(f"Failed to fetch job post content. Status code: {response.status_code}")
            return None
            #raise Exception("Failed to fetch job post content.")
            
        
        
