from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, deps

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

@router.get("/")
def get_users(db: Session = Depends(deps.get_db)):
    users = crud.get_users(db=db)
    # print(users)
    return users

@router.get("/{username}")
def get_user_name(username: str, db: Session = Depends(deps.get_db)):
    user = crud.get_user(db=db, username=username)
    if user:
        return user.__delattr__("password")
    else:
        raise HTTPException(status_code=404, detail="User not found")
