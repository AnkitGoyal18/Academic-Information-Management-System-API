from fastapi import FastAPI, Depends, status, Response
from users import models
from users.database import engine
from users.routers import user

app = FastAPI()

app.include_router(user.router)

models.Base.metadata.create_all(engine)

if __name__ == "__main__":
    models.Base.metadata.create_all(engine)
