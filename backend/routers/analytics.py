"""Analytics router."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from database import get_db
from models import User, Prospect, Activity
from schemas import DashboardMetrics, ActivityStats
from auth import get_current_user

router = APIRouter()


@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard metrics."""
    # Count prospects by status
    total_prospects = db.query(Prospect).filter(Prospect.user_id == current_user.id).count()
    new_prospects = db.query(Prospect).filter(
        Prospect.user_id == current_user.id,
        Prospect.status == "new"
    ).count()
    contacted = db.query(Prospect).filter(
        Prospect.user_id == current_user.id,
        Prospect.status == "contacted"
    ).count()
    connected = db.query(Prospect).filter(
        Prospect.user_id == current_user.id,
        Prospect.status == "connected"
    ).count()
    replied = db.query(Prospect).filter(
        Prospect.user_id == current_user.id,
        Prospect.status == "replied"
    ).count()
    qualified = db.query(Prospect).filter(
        Prospect.user_id == current_user.id,
        Prospect.status == "qualified"
    ).count()
    
    # Calculate acceptance rate
    acceptance_rate = 0.0
    if contacted > 0:
        acceptance_rate = (connected / contacted) * 100
    
    # Get today's activity count
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    daily_activity = db.query(Activity).filter(
        Activity.user_id == current_user.id,
        Activity.created_at >= today_start,
        Activity.activity_type.in_(['connection_sent', 'email_sent'])
    ).count()
    
    return {
        "total_prospects": total_prospects,
        "new_prospects": new_prospects,
        "contacted": contacted,
        "connected": connected,
        "replied": replied,
        "qualified": qualified,
        "connection_acceptance_rate": round(acceptance_rate, 1),
        "daily_activity_count": daily_activity,
        "daily_limit": 20
    }


@router.get("/activity-stats")
async def get_activity_stats(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get activity statistics for the last N days."""
    start_date = datetime.now() - timedelta(days=days)
    
    # Query activities grouped by date
    activities = db.query(
        func.date(Activity.created_at).label('date'),
        func.count(Activity.id).label('count')
    ).filter(
        Activity.user_id == current_user.id,
        Activity.created_at >= start_date
    ).group_by(
        func.date(Activity.created_at)
    ).all()
    
    # Format results
    stats = [
        {"date": str(activity.date), "count": activity.count}
        for activity in activities
    ]
    
    return stats


@router.get("/pipeline-stats")
async def get_pipeline_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pipeline statistics."""
    # Count prospects by status
    pipeline = db.query(
        Prospect.status,
        func.count(Prospect.id).label('count')
    ).filter(
        Prospect.user_id == current_user.id
    ).group_by(
        Prospect.status
    ).all()
    
    # Format results
    stats = {
        status: count
        for status, count in pipeline
    }
    
    return stats
