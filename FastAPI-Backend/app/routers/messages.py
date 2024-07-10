from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from .. import schemas, crud, deps
from datetime import datetime

router = APIRouter(
    prefix="/api/v1/messages",
    tags=["messages"]
)

@router.post("/")
def add_message(
    chatID: str = Form(...),
    message: Optional[str] = Form(None),
    sender: str = Form(...),
    isFile: bool = Form(...),
    mimeType: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(deps.get_db)
):
    if(message == None and file == None):    
        raise HTTPException(status_code=400, detail="Message or file is required")
    if(message == None):
        message = ""
    filename = ""
    if file:
        filename = chatID + str(datetime.now()) + file.filename.split(".")[-1]
        filename = filename.replace(":", "-").replace(" ", "-")
        with open(f"files/{filename}", "wb") as buffer:
            buffer.write(file.file.read())

    created_message = schemas.MessageCreate(chatID=chatID, message=message, sender=sender, isFile=isFile, mimeType=mimeType, filename=filename)
    crud.create_message(db=db, message=created_message)
    return crud.get_messages(db=db, chatID=chatID)

@router.get("/")
def get_messages(chatID: str, db: Session = Depends(deps.get_db)):
    messages = crud.get_messages(db=db, chatID=chatID)
    if not messages:
        return []
    # print(messages)
    return messages
