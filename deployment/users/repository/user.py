from fastapi import status, Response
from users import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import uuid4


def create(user: schemas.User, response: Response, db: Session):
    check_user = db.query(models.User).filter(or_(models.User.registerNumber == user.registerNumber,
                                                  models.User.personalEmail == user.personalEmail, models.User.officialEmail == user.officialEmail)).first()
    if not check_user:
        user.id = user.registerNumber
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"data": new_user, "status": "success", "code": "SUCCESS"}
    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"data": f"User already exists", "status": "failure", "code": "FAILURE"}


def get_all(response: Response, db: Session):
    users = db.query(models.User).all()
    if users.__len__():
        return {"data": users, "count": users.__len__()}
    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"data": "There are no users in the database", "count": 0}


def get_by_id(id: str, response: Response, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"User with the id {id} is not available"}
    return {"data": user}

def update_by_id(id: str, user: schemas.User, db: Session):
    user.id = id
    current_user = db.query(models.User).filter(
        models.User.id == id).update(user.dict())
    db.commit()
    if current_user:
        return {"data": user, "status": "updated", "code": "UPDATED"}
    return {"data": "Fail to update the User"}


def delete_all(db: Session):
    db.query(models.User).delete(synchronize_session=False)
    db.commit()
    return {"data": "All users deleted"}


def delete_by_id(id: str, response: Response, db: Session):
    current_user = db.query(models.User).filter(models.User.id == id)
    if current_user.first():
        current_user.delete(synchronize_session=False)
        db.commit()
        return {"data": f"User with id {id} is deleted successfully"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data": f"User with the id {id} doesn't exist"}
