from fastapi import APIRouter, status, Response, Depends
from users import schemas, models, database
from sqlalchemy import or_
from uuid import uuid4
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, response: Response, db: Session = Depends(database.get_db)):
    check_user = db.query(models.User).filter(or_(models.User.registerNumber == user.registerNumber,
                                                  models.User.personalEmail == user.personalEmail, models.User.officialEmail == user.officialEmail)).first()
    if not check_user:
        user.id = uuid4().hex
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"data": new_user, "status": "success", "code": "SUCCESS"}
    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"data": f"User already exists", "status": "failure", "code": "FAILURE"}


@router.get("/")
def all_users(response: Response, db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    if users.__len__():
        return {"data": users, "count": users.__len__()}
    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"data": "There are no users in the database", "count": 0}


@router.get("/{id}")
def get_user_by_id(id: str, response: Response, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"User with the id {id} is not available"}
    return {"data": user}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user_by_id(id: str, user: schemas.User, db: Session = Depends(database.get_db)):
    user.id = id
    current_user = db.query(models.User).filter(
        models.User.id == id).update(user.dict())
    db.commit()
    if current_user:
        return {"data": user, "status": "updated", "code": "UPDATED"}
    return {"data": "Fail to update the User"}


@router.delete("/")
def all_users(db: Session = Depends(database.get_db)):
    db.query(models.User).delete(synchronize_session=False)
    db.commit()
    return {"data": "All users deleted"}


@router.delete("/{id}")
def delete_user_by_id(id: str, response: Response, db: Session = Depends(database.get_db)):
    current_user = db.query(models.User).filter(models.User.id == id)
    if current_user.first():
        current_user.delete(synchronize_session=False)
        db.commit()
        return {"data": f"User with id {id} is deleted successfully"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data": f"User with the id {id} doesn't exist"}