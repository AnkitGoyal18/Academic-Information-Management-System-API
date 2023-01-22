from fastapi import APIRouter, status, Response, Depends
from users import schemas, database
from sqlalchemy.orm import Session
from users.repository import user as userHelper


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, response: Response, db: Session = Depends(database.get_db)):
    return userHelper.create(user=user, response=response, db=db)


@router.get("/")
def all_users(response: Response, db: Session = Depends(database.get_db)):
    return userHelper.get_all(response=response, db=db)


@router.get("/{id}")
def get_user_by_id(id: str, response: Response, db: Session = Depends(database.get_db)):
    return userHelper.get_by_id(id=id, response=response, db=db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user_by_id(id: str, user: schemas.User, db: Session = Depends(database.get_db)):
    return userHelper.update_by_id(id=id, user=user, db=db)


@router.delete("/")
def all_users(db: Session = Depends(database.get_db)):
    return userHelper.delete_all(db=db)


@router.delete("/{id}")
def delete_user_by_id(id: str, response: Response, db: Session = Depends(database.get_db)):
    return userHelper.delete_by_id(id=id, response=response, db=db)
