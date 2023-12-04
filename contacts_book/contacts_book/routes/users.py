from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from contacts_book.database.db import get_db
from contacts_book.database.models import User
from contacts_book.repository import users as repository_users
from contacts_book.services.auth import auth_service
from contacts_book.conf.config import settings
from contacts_book.schemas import UserDb
from contacts_book.services.cloud_image import CloudImage

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    public_id = CloudImage.generate_name_avatar(current_user.email)
    r = CloudImage.upload(file.file, public_id)
    src_url = CloudImage.get_url_for_avatar(public_id, r)
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user