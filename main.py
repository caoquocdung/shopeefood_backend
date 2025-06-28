from fastapi import FastAPI

from routers import address, user

app = FastAPI()

app.include_router(user.router)
app.include_router(address.router)