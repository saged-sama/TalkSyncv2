from fastapi import Form, File, UploadFile, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud, deps

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

@router.post("/register")
def register(
    username: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(deps.get_db)
):
    imgfilename = image.filename
    imagepath = f"files/{username}{imgfilename}"

    user = schemas.UserCreate(username=username, password=password, name=name, image=f"{username}{imgfilename}")
    created_user = crud.create_user(db, user)
    if created_user:
        with open(imagepath, "wb") as buffer:
            buffer.write(image.file.read())
    return {
        "message": "user registration successful",
        "user": created_user
    }

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(deps.get_db)
):
    db_user = crud.get_user(db=db, username=username)
    if db_user and db_user.password == password:
        return {
            "message": "login successful"
        }
    else:
        raise HTTPException(status_code=401, detail="unauthorized")
