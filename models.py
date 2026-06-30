from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional
from logger import logger


class Job(BaseModel):
    """
    Pydantic model for validating job data.
    Ensures data integrity before storing in database.
    """
    job_id: str = Field(..., min_length=1, description="Unique job identifier (slugified company-title)")
    job_title: str = Field(..., min_length=1, max_length=255, description="Job title")
    company: str = Field(..., min_length=1, max_length=255, description="Company name")
    location: str = Field(..., min_length=1, max_length=255, description="Job location")
    application_link: str = Field(..., description="URL to apply for the job")
    skills_list: List[str] = Field(default_factory=list, description="Required skills")

    @validator('job_title', 'company', 'location', pre=True)
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace from string fields"""
        if isinstance(v, str):
            return v.strip()
        return v

    @validator('job_id', pre=True)
    def validate_job_id(cls, v):
        """Ensure job_id is not empty after stripping"""
        if isinstance(v, str):
            v = v.strip().lower().replace(' ', '-')
        if not v:
            raise ValueError('job_id cannot be empty')
        return v

    @validator('application_link', pre=True)
    def validate_url(cls, v):
        """Validate that application_link is a valid URL"""
        if not v:
            raise ValueError('application_link cannot be empty')
        v = str(v).strip()
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError(f'application_link must start with http:// or https://, got: {v}')
        return v

    @validator('skills_list', pre=True)
    def clean_skills(cls, v):
        """Clean and deduplicate skills list"""
        if not isinstance(v, list):
            return []
        # Filter out empty strings and deduplicate
        skills = [skill.strip().lower() for skill in v if isinstance(skill, str) and skill.strip()]
        return list(set(skills))  # Remove duplicates

    class Config:
        """Pydantic config"""
        str_strip_whitespace = True
        use_enum_values = True


class JobList(BaseModel):
    """
    Wrapper for validating a list of jobs
    """
    jobs: List[Job]

    def validate_all(self) -> tuple[List[Job], List[dict]]:
        """
        Validate all jobs and return valid jobs + errors.
        
        Returns:
            Tuple of (valid_jobs, invalid_jobs_with_errors)
        """
        valid_jobs = []
        invalid_jobs = []

        for i, job_data in enumerate(self.jobs):
            try:
                # Try to validate each job
                valid_job = Job(**job_data if isinstance(job_data, dict) else job_data.dict())
                valid_jobs.append(valid_job)
            except Exception as e:
                logger.warning(f"Invalid job at index {i}: {str(e)}")
                invalid_jobs.append({
                    'index': i,
                    'error': str(e),
                    'data': job_data
                })

        return valid_jobs, invalid_jobs
