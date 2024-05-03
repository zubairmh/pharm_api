from routers import cart
from routers import auth
from fastapi import FastAPI

app=FastAPI()
app.include_router(auth.router)
app.include_router(cart.router)