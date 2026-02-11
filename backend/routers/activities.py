"""Activities router."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from database import get_db
from models import User, Activity
from schemas import ActivityCreate, ActivityResponse
from auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ActivityResponse])
async def get_activities(
    skip: int = 0,
    limit: int = 100,
    activity_type: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all activities for current user."""
    query = db.query(Activity).filter(Activity.user_id == current_user.id)
    
    if activity_type:
        query = query.filter(Activity.activity_type == activity_type)
    
    activities = query.order_by(Activity.created_at.desc()).offset(skip).limit(limit).all()
    return activities


@router.post("/", response_model=ActivityResponse)
async def create_activity(
    activity: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new activity log entry."""
    db_activity = Activity(
        user_id=current_user.id,
        prospect_id=activity.prospect_id,
        activity_type=activity.activity_type,
        description=activity.description
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity


@router.get("/today-count")
async def get_today_activity_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get activity count for today."""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    count = db.query(Activity).filter(
        Activity.user_id == current_user.id,
        Activity.created_at >= today_start,
        Activity.activity_type.in_(['connection_sent', 'email_sent'])
    ).count()
    
    return {
        "count": count,
        "limit": 20,
        "remaining": max(0, 20 - count)
    }
