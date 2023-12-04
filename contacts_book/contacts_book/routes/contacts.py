from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from contacts_book.database.db import get_db
from contacts_book.database.models import User
from contacts_book.schemas import ContactModel, ContactResponce
from contacts_book.repository import contacts as repository_contacts
from contacts_book.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get(
    "/",
    response_model=List[ContactResponce],
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    name="Read contacts",
)
async def get_contacts(
    limit: int = Query(10, le=100),
    offset: int = 0,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_contacts.get_contacts(
        limit, offset, search, current_user, db
    )


@router.get(
    "/upcoming_birthdays",
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    name="Upcoming birthdays",
)
async def get_contact(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_contacts.get_upcoming_birthdays(current_user, db)


@router.get(
    "/{contact_id}",
    response_model=ContactResponce,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    name="Read contact",
)
async def get_contact(
    contact_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found!"
        )

    return contact


@router.post(
    "/",
    response_model=ContactResponce,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=30))],
    name="Create contact",
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    body: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.get_contact_by_unique_fields(
        body, current_user, db
    )

    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with such unique fields is exists!",
        )

    contact = await repository_contacts.create_contact(body, current_user, db)

    return contact


@router.put(
    "/{contact_id}",
    response_model=ContactResponce,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=30))],
    name="Read contact",
)
async def update_contact(
    body: ContactModel,
    contact_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.get_contact_by_unique_fields(
        body, current_user, db
    )

    if contact and contact.id != contact_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with such unique fields is exists!",
        )

    contact = await repository_contacts.update_contact(
        body, contact_id, current_user, db
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found!"
        )

    return contact


@router.delete(
    "/{contact_id}",
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=30))],
    name="Delete contact",
)
async def delete_contact(
    contact_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found!"
        )

    return contact
