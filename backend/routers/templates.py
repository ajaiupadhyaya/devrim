"""Templates router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, Template, Prospect
from schemas import (
    TemplateCreate,
    TemplateResponse,
    TemplateUpdate,
    MessageComposeRequest,
    MessageComposeResponse
)
from auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[TemplateResponse])
async def get_templates(
    category: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all templates for current user."""
    query = db.query(Template).filter(Template.user_id == current_user.id)
    
    if category:
        query = query.filter(Template.category == category)
    
    templates = query.all()
    return templates


@router.post("/", response_model=TemplateResponse)
async def create_template(
    template: TemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new template."""
    db_template = Template(
        user_id=current_user.id,
        title=template.title,
        category=template.category,
        content=template.content,
        times_used=0
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    return db_template


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific template."""
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return template


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: int,
    template_update: TemplateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a template."""
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Update fields
    update_data = template_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a template."""
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    db.delete(template)
    db.commit()
    
    return {"message": "Template deleted successfully"}


@router.post("/compose", response_model=MessageComposeResponse)
async def compose_message(
    request: MessageComposeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compose a message from template with prospect data."""
    # Get template
    template = db.query(Template).filter(
        Template.id == request.template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Get prospect
    prospect = db.query(Prospect).filter(
        Prospect.id == request.prospect_id,
        Prospect.user_id == current_user.id
    ).first()
    
    if not prospect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect not found"
        )
    
    # Get company name
    company_name = ""
    if prospect.company_id:
        from models import Company
        company = db.query(Company).filter(Company.id == prospect.company_id).first()
        if company:
            company_name = company.name
    
    # Replace variables
    message = template.content
    replacements = {
        "{first_name}": prospect.first_name or "",
        "{last_name}": prospect.last_name or "",
        "{full_name}": prospect.full_name or "",
        "{company}": company_name,
        "{position}": prospect.position or "",
        "{sector}": prospect.sector or "",
        "{custom_note}": request.custom_note or "",
        "{my_name}": current_user.full_name or "",
        "{my_company}": current_user.company or "",
        "{my_position}": current_user.position or ""
    }
    
    for placeholder, value in replacements.items():
        message = message.replace(placeholder, value)
    
    # Update template usage count
    template.times_used += 1
    db.commit()
    
    return {
        "message": message,
        "character_count": len(message)
    }
