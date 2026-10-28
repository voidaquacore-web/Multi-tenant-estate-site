from typing import Literal, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from routers.auth import current_user
from db import get_conn

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

@router.get('/{listing_id}')
def get_listing(listing_id: str, user=Depends(current_user)):
    with get_conn() as conn:
        r = conn.execute(
            'SELECT id, title, description, price, type, beds, baths, area, city, status, photo_urls '
            'FROM listings WHERE id = %s AND agency_id = %s',
            (listing_id, user['agency_id'])
        ).fetchone()
    if not r:
        raise HTTPException(404, 'Listing not found')
    return    { 
             'id': str(r[0]), 'title': r[1], 'description': r[2], 'price': float(r[3]), 'type' :r[4], 'beds':r[5],  'baths':r[6],  'area': r[7],
             'city': r[8], 'status': r[9], 'photo_urls': r[10]
             }

@router.put('/{listing_id}')
def update_listing(listing_id: str, body: ListingBody, user=Depends(current_user)):
    with get_conn() as conn:
        r = conn.execute(
            'UPDATE listings SET title=%s, description=%S, price%s, type=%s, beds=%s, baths=%s, area=%s, city=%s '
            'WHERE id = %s AND agency_id = %s RETURNING id', 
            (body.title, body.description, body.price, body.type, body.beds, body.baths, body.area, body.city, listing_id, user['agency_id'])
        ).fetchone()
        if not r:
                raise HTTPException(404, 'Listing not found')
        return {'id': str(r[0])}

@router.delete('/{listing_id}')
def delete_listing(listing_id: str, user=Depends(current_user)):
    with get_conn() as conn:
        r = conn.execute(
            'DELETE FROM listings WHERE id = %s AND agency_id =%s RETURNING id', 
            (listing_id, user['agency_id'])
        ).fetchone()
    if not r:
        raise HTTPException(404, 'Listing not found')
    return {'deleted': True}