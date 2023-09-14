from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models
import schemas


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        birth_date=contact.birth_date,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: schemas.ContactCreate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        contact_data = contact.model_dict
        for key, value in contact_data.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact


def search_contacts(db: Session, query: str):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.ilike(f"%{query}%")) |
        (models.Contact.last_name.ilike(f"%{query}%")) |
        (models.Contact.email.ilike(f"%{query}%")) |
        (models.Contact.phone_number.ilike(f"%{query}%"))
    ).all()


def get_upcoming_birthdays(db: Session):
    today = datetime.now()
    week_from_today = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        (models.Contact.birth_date >= today) &
        (models.Contact.birth_date <= week_from_today)
    ).all()

