from fastapi import FastAPI, Depends, status, Response
from users import schemas, models
from users.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import uuid4

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: schemas.User, response: Response, db: Session = Depends(get_db)):
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


@app.get("/users", tags=["Users"])
def all_users(response: Response, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if users.__len__():
        return {"data": users, "count": users.__len__()}
    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"data": "There are no users in the database", "count": 0}


@app.get("/users/{id}", tags=["Users"])
def get_user_by_id(id: str, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"User with the id {id} is not available"}
    return {"data": user}


@app.put("/users/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
def update_user_by_id(id: str, user: schemas.User, db: Session = Depends(get_db)):
    user.id = id
    current_user = db.query(models.User).filter(
        models.User.id == id).update(user.dict())
    db.commit()
    if current_user:
        return {"data": user, "status": "updated", "code": "UPDATED"}
    return {"data": "Fail to update the User"}


@app.delete("/users", tags=["Users"])
def all_users(db: Session = Depends(get_db)):
    db.query(models.User).delete(synchronize_session=False)
    db.commit()
    return {"data": "All users deleted"}


@app.delete("/users/{id}", tags=["Users"])
def delete_user_by_id(id: str, response: Response, db: Session = Depends(get_db)):
    current_user = db.query(models.User).filter(models.User.id == id)
    if current_user.first():
        current_user.delete(synchronize_session=False)
        db.commit()
        return {"data": f"User with id {id} is deleted successfully"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data": f"User with the id {id} doesn't exist"}


if __name__ == "__main__":
    models.Base.metadata.create_all(engine)
