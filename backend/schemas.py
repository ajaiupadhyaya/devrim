"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Prospect schemas
class ProspectBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: str
    position: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    sector: Optional[str] = None
    custom_tags: Optional[str] = None
    notes: Optional[str] = None
    company_name: Optional[str] = None


class ProspectCreate(ProspectBase):
    pass


class ProspectUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    linkedin_url: Optional[str] = None
    sector: Optional[str] = None
    custom_tags: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    last_contacted: Optional[datetime] = None


class ProspectResponse(ProspectBase):
    id: int
    user_id: int
    company_id: Optional[int] = None
    email_verified: bool
    status: str
    last_contacted: Optional[datetime] = None
    added_date: datetime
    
    class Config:
        from_attributes = True


# Company schemas
class CompanyBase(BaseModel):
    name: str
    domain: Optional[str] = None
    sector: Optional[str] = None
    notes: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Template schemas
class TemplateBase(BaseModel):
    title: str
    category: Optional[str] = None
    content: str


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None


class TemplateResponse(TemplateBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    times_used: int
    
    class Config:
        from_attributes = True


# Activity schemas
class ActivityBase(BaseModel):
    activity_type: str
    description: Optional[str] = None
    prospect_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# CSV Import schema
class CSVImportRequest(BaseModel):
    prospects: List[ProspectCreate]


# Email finder schema
class EmailFinderRequest(BaseModel):
    full_name: str
    company_domain: str


class EmailFinderResponse(BaseModel):
    email: Optional[str] = None
    verified: bool = False
    confidence: Optional[str] = None


# Message composer schema
class MessageComposeRequest(BaseModel):
    template_id: int
    prospect_id: int
    custom_note: Optional[str] = None


class MessageComposeResponse(BaseModel):
    message: str
    character_count: int


# Analytics schemas
class DashboardMetrics(BaseModel):
    total_prospects: int
    new_prospects: int
    contacted: int
    connected: int
    replied: int
    qualified: int
    connection_acceptance_rate: float
    daily_activity_count: int
    daily_limit: int


class ActivityStats(BaseModel):
    date: str
    count: int
