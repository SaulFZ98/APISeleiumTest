from platform import version

from fastapi import FastAPI
from api.routes import users


app = FastAPI(
    title="User API for Test Atomation",
    version ="1.0.0"
)

app.include_router(users.router)