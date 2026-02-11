"""Prospects router."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from datetime import datetime

from database import get_db
from models import User, Prospect, Company, Activity
from schemas import (
    ProspectCreate,
    ProspectResponse,
    ProspectUpdate,
    EmailFinderRequest,
    EmailFinderResponse
)
from auth import get_current_user
from email_finder import EmailFinderService

router = APIRouter()


@router.get("/", response_model=List[ProspectResponse])
async def get_prospects(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all prospects for current user."""
    query = db.query(Prospect).filter(Prospect.user_id == current_user.id)
    
    if status:
        query = query.filter(Prospect.status == status)
    
    prospects = query.offset(skip).limit(limit).all()
    return prospects


@router.post("/", response_model=ProspectResponse)
async def create_prospect(
    prospect: ProspectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new prospect."""
    # Check for duplicates
    existing = db.query(Prospect).filter(
        Prospect.user_id == current_user.id,
        Prospect.full_name == prospect.full_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prospect with this name already exists"
        )
    
    # Create or get company
    company_id = None
    if prospect.company_name:
        company = db.query(Company).filter(Company.name == prospect.company_name).first()
        if not company:
            company = Company(name=prospect.company_name, sector=prospect.sector)
            db.add(company)
            db.commit()
            db.refresh(company)
        company_id = company.id
    
    # Create prospect
    db_prospect = Prospect(
        user_id=current_user.id,
        company_id=company_id,
        first_name=prospect.first_name,
        last_name=prospect.last_name,
        full_name=prospect.full_name,
        position=prospect.position,
        email=prospect.email,
        linkedin_url=prospect.linkedin_url,
        sector=prospect.sector,
        custom_tags=prospect.custom_tags,
        notes=prospect.notes,
        status="new"
    )
    
    db.add(db_prospect)
    db.commit()
    db.refresh(db_prospect)
    
    # Log activity
    activity = Activity(
        user_id=current_user.id,
        prospect_id=db_prospect.id,
        activity_type="prospect_added",
        description=f"Added prospect: {prospect.full_name}"
    )
    db.add(activity)
    db.commit()
    
    return db_prospect


@router.get("/{prospect_id}", response_model=ProspectResponse)
async def get_prospect(
    prospect_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific prospect."""
    prospect = db.query(Prospect).filter(
        Prospect.id == prospect_id,
        Prospect.user_id == current_user.id
    ).first()
    
    if not prospect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect not found"
        )
    
    return prospect


@router.put("/{prospect_id}", response_model=ProspectResponse)
async def update_prospect(
    prospect_id: int,
    prospect_update: ProspectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a prospect."""
    prospect = db.query(Prospect).filter(
        Prospect.id == prospect_id,
        Prospect.user_id == current_user.id
    ).first()
    
    if not prospect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect not found"
        )
    
    # Update fields
    update_data = prospect_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prospect, field, value)
    
    db.commit()
    db.refresh(prospect)
    
    # Log status change if status was updated
    if prospect_update.status:
        activity = Activity(
            user_id=current_user.id,
            prospect_id=prospect.id,
            activity_type="status_changed",
            description=f"Status changed to: {prospect_update.status}"
        )
        db.add(activity)
        db.commit()
    
    return prospect


@router.delete("/{prospect_id}")
async def delete_prospect(
    prospect_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a prospect."""
    prospect = db.query(Prospect).filter(
        Prospect.id == prospect_id,
        Prospect.user_id == current_user.id
    ).first()
    
    if not prospect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect not found"
        )
    
    db.delete(prospect)
    db.commit()
    
    return {"message": "Prospect deleted successfully"}


@router.post("/import-csv")
async def import_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Import prospects from CSV file."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV"
        )
    
    # Read CSV
    contents = await file.read()
    csv_data = io.StringIO(contents.decode('utf-8'))
    reader = csv.DictReader(csv_data)
    
    imported = 0
    skipped = 0
    errors = []
    
    for row in reader:
        try:
            # Map CSV columns to prospect fields
            company_name = row.get('company', '').strip()
            full_name = row.get('name', row.get('full_name', '')).strip()
            
            if not full_name or not company_name:
                skipped += 1
                continue
            
            # Check for duplicates
            existing = db.query(Prospect).filter(
                Prospect.user_id == current_user.id,
                Prospect.full_name == full_name
            ).first()
            
            if existing:
                skipped += 1
                continue
            
            # Get or create company
            company = db.query(Company).filter(Company.name == company_name).first()
            if not company:
                company = Company(
                    name=company_name,
                    sector=row.get('sector', '').strip()
                )
                db.add(company)
                db.commit()
                db.refresh(company)
            
            # Create prospect
            prospect = Prospect(
                user_id=current_user.id,
                company_id=company.id,
                full_name=full_name,
                position=row.get('desired_role', row.get('position', '')).strip(),
                sector=row.get('sector', '').strip(),
                email=row.get('email', '').strip() if row.get('email') else None,
                linkedin_url=row.get('linkedin_url', '').strip() if row.get('linkedin_url') else None,
                status="new"
            )
            
            db.add(prospect)
            imported += 1
            
        except Exception as e:
            errors.append(f"Row error: {str(e)}")
            skipped += 1
    
    db.commit()
    
    # Log activity
    activity = Activity(
        user_id=current_user.id,
        activity_type="csv_import",
        description=f"Imported {imported} prospects from CSV"
    )
    db.add(activity)
    db.commit()
    
    return {
        "message": "CSV import completed",
        "imported": imported,
        "skipped": skipped,
        "errors": errors
    }


@router.post("/find-email", response_model=EmailFinderResponse)
async def find_email(
    request: EmailFinderRequest,
    current_user: User = Depends(get_current_user)
):
    """Find email for a prospect."""
    result = await EmailFinderService.find_email(
        request.full_name,
        request.company_domain
    )
    return result
