"""
Task 1: Structured LLM Prompt Pipeline & JSON Extractor
Pydantic v2 Resume Schemas with professional history and skills categorization.
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class WorkExperience(BaseModel):
    company: str = Field(..., description="Name of employer or organization")
    job_title: str = Field(..., description="Official title or designation")
    start_date: str = Field(..., description="Start date (e.g., '2022-01' or 'Jan 2022')")
    end_date: Optional[str] = Field("Present", description="End date or 'Present'")
    location: Optional[str] = Field(None, description="City, State, Country or 'Remote'")
    achievements: List[str] = Field(default_factory=list, description="Key measurable accomplishments and duties")
    skills_used: List[str] = Field(default_factory=list, description="Technologies or methodologies leveraged")


class Education(BaseModel):
    institution: str = Field(..., description="University, college, or training institution")
    degree: str = Field(..., description="Degree obtained e.g. B.S., M.S., Ph.D.")
    field_of_study: Optional[str] = Field(None, description="Major / concentration")
    graduation_year: Optional[int] = Field(None, ge=1960, le=2035, description="Four-digit graduation year")
    gpa: Optional[str] = Field(None, description="Reported GPA or grade classification")


class SkillsInventory(BaseModel):
    programming_languages: List[str] = Field(default_factory=list)
    frameworks_and_libraries: List[str] = Field(default_factory=list)
    cloud_and_devops: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    tools_and_methods: List[str] = Field(default_factory=list)


class ResumeSchema(BaseModel):
    candidate_name: str = Field(..., description="Full legal or professional name of the candidate")
    email: str = Field(..., description="Primary contact email address")
    phone: Optional[str] = Field(None, description="Phone number with country or area code")
    location: Optional[str] = Field(None, description="Current geographical location")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    github_url: Optional[str] = Field(None, description="GitHub portfolio URL")
    professional_summary: str = Field(..., description="2-4 sentence executive biography")
    experience: List[WorkExperience] = Field(default_factory=list, description="Chronological work history")
    education: List[Education] = Field(default_factory=list, description="Academic credentials")
    skills: SkillsInventory = Field(default_factory=SkillsInventory, description="Categorized technical competencies")
    certifications: List[str] = Field(default_factory=list, description="Professional certifications or licenses")

    @field_validator("candidate_name")
    @classmethod
    def clean_name(cls, v: str) -> str:
        cleaned = v.strip().title()
        if len(cleaned) < 2:
            raise ValueError("Candidate name must contain at least 2 characters.")
        return cleaned
