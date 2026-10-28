from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import router as auth_router
from routers.listings import router as listing_router
from db import get_conn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth_router)
app.include_router(listing_router)

@app.get('/')
def root():
    return {'message': 'All good'}
