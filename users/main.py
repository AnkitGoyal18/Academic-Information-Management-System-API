from fastapi import FastAPI
from users import schemas, models
from users.database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.post("/users")
def create_user(user: schemas.User):
    return {"data": user, "status": "success", "code": "SUCCESS"}


@app.get("/users")
def all_users():
    return "Hello"
