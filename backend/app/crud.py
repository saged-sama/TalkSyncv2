from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        password=user.password,
        name=user.name,
        image=user.image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def create_message(db: Session, message: schemas.MessageCreate):
    new_message = models.ChatMessage(
        chat_id=message.chatID,
        sender=message.sender,
        time=datetime.now(),
        message=message.message,
        is_file=message.isFile,
        mime_type=message.mimeType,
        filename=message.filename,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def get_messages(db: Session, chatID: str):
    return db.query(models.ChatMessage).filter(models.ChatMessage.chat_id == chatID).all()
