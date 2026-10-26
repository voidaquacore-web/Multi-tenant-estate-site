from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from db import get_conn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth_router)

@app.get('/')
def root():
    return {'message': 'All good'}

@app.get('/db-check')
def deb_check():
    with get_conn() as conn:
        row = conn.execute('SELECT (name) FROM agencies').fetchone()
        return {'agency': row[0],
                }