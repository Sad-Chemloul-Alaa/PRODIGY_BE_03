from fastapi import FastAPI
from app.api import authentification ,user as api_user
from app.core.database import engine
from app.models import user as models

app = FastAPI()
models.Base.metadata.create_all(engine)
app.include_router(api_user.router)
app.include_router(authentification.router)