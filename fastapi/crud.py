from sqlalchemy.orm import Session
import models
from models import Listing

def get_listings(db: Session, location: str = None, min_price: int = None, max_price: int = None):
    query = db.query(Listing)

    if location:
        query = query.filter(Listing.location.ilike(f"%{location}%"))
    if min_price is not None:
        query = query.filter(Listing.rent_price >= min_price)
    if max_price is not None:
        query = query.filter(Listing.rent_price <= max_price)

    return query.all()
