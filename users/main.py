from fastapi import FastAPI, Depends, status, Response
from users import schemas, models
from users.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", status_code=status.HTTP_201_CREATED )
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user.id = 1
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": user, "status": "success", "code": "SUCCESS"}


@app.get("/users")
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"data": users, "count": users.__len__()}

@app.get("/users/{id}")
def get_user_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"data": f"User with the id {id} is not available"}
    return {"data": user}

@app.put("/users/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user_by_id(id: int, user: schemas.User, db: Session = Depends(get_db)):
    current_user = db.query(models.User).filter(models.User.id == id).update(user)
    current_user.update(user.dict())
    db.commit()
    return {"data":user}

@app.delete("/users")
def all_users(db: Session = Depends(get_db)):
    db.query(models.User).delete(synchronize_session=False)
    db.commit()
    return {"data": "All users deleted"}

@app.delete("/users/{id}")
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data": f"User with id {id} is deleted successfully"}