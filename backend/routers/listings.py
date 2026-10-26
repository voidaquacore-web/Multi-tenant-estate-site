from typing import Literal, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from auth import current_user
from backend.db import get_conn

router = APIRouter(prefix="/listings", tags=['listings'])

class ListingBody(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: Optional[str] = None
    price: float= Field(gt=0)
    type: Literal['sale', 'rent']
    beds: Optional[int] = Field(default=None, gt=0)
    baths: Optional[int] = Field(default=None, gt=0)
    area: Optional[int] = Field(default=None, gt=0)
    city: str = Field(min_length=2, max_length=100)

@router.post('')
def create_listing(body: ListingBody, user=Depends(current_user)):
    with get_conn as conn:
        row = conn.execute(
            "INSERT INTO listings (agency_id, title, description, price, type, beds, baths, area, city) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (user['agency_id'], body.title, body.description, body.price, body.type, body.beds, body.baths, body.area, body.city),
        ).fetchone()
        return {'id': str[row[0]]}
@router.get('')
def my_listings(user=Depends(current_user)):
    with get_conn as conn:
        row = conn.execute(
            "SELECT id, title, price, type, beds, baths, city, status"
            "FROM listings WHERE  agency_id = %s ORDER BY created_at DESC",
            (user['agency_id'],),
        )
    return [
        {
         'id': str(row[0]),
         'title': row[1],
         'price': row[2],
         'type' :row[3],
         'beds' :row[4],
         'baths':row[5],
         'city':row[6],
         'status':row[7],
         }
    ]