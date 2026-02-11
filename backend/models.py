"""Database models for Smart Outreach Dashboard."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """User model for authentication."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    company = Column(String)
    position = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    prospects = relationship("Prospect", back_populates="user")
    templates = relationship("Template", back_populates="user")
    activities = relationship("Activity", back_populates="user")


class Company(Base):
    """Company model for grouping prospects."""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    domain = Column(String, index=True)
    sector = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    prospects = relationship("Prospect", back_populates="company")


class Prospect(Base):
    """Prospect model for managing leads."""
    
    __tablename__ = "prospects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    # Personal info
    first_name = Column(String)
    last_name = Column(String)
    full_name = Column(String, nullable=False)
    position = Column(String)
    
    # Contact info
    email = Column(String, index=True)
    email_verified = Column(Boolean, default=False)
    linkedin_url = Column(String)
    
    # Categorization
    sector = Column(String)
    custom_tags = Column(String)  # Comma-separated tags
    
    # Pipeline status
    status = Column(String, default="new")  # new, contacted, connected, replied, qualified, unqualified, dead
    
    # Tracking
    last_contacted = Column(DateTime(timezone=True))
    added_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="prospects")
    company = relationship("Company", back_populates="prospects")
    activities = relationship("Activity", back_populates="prospect")


class Template(Base):
    """Message template model."""
    
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    category = Column(String)  # linkedin_connection, linkedin_followup, email_initial, email_followup
    content = Column(Text, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    times_used = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="templates")


class Activity(Base):
    """Activity log for tracking all actions."""
    
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prospect_id = Column(Integer, ForeignKey("prospects.id"))
    
    activity_type = Column(String, nullable=False)  # connection_sent, email_sent, note_added, status_changed
    description = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="activities")
    prospect = relationship("Prospect", back_populates="activities")


class EmailSequence(Base):
    """Email sequence for automated follow-ups."""
    
    __tablename__ = "email_sequences"
    
    id = Column(Integer, primary_key=True, index=True)
    prospect_id = Column(Integer, ForeignKey("prospects.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"))
    
    sequence_number = Column(Integer, nullable=False)
    scheduled_date = Column(DateTime(timezone=True))
    sent_date = Column(DateTime(timezone=True))
    status = Column(String, default="pending")  # pending, sent, failed
    
    # Tracking
    opened = Column(Boolean, default=False)
    clicked = Column(Boolean, default=False)
    replied = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
