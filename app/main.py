from fastapi import FastAPI
from .routers import users, login, products, orders, carts
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


origins = [
    "http://localhost:8000","https://resttesttest.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.routers)
app.include_router(login.routers)
app.include_router(products.routers)
app.include_router(orders.routers)
app.include_router(carts.routers)

@app.get("/")
def first():
    return {"message": "Hello World"}
