from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/listings/", response_model=schemas.Listing)
def create_listing(listing: schemas.ListingCreate, db: Session = Depends(get_db)):
    db_listing = models.Listing(**listing.dict())
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@app.get("/listings/", response_model=list[schemas.Listing])
def read_listings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Listing).offset(skip).limit(limit).all()

@app.get("/listings/{listing_id}", response_model=schemas.Listing)
def read_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@app.put("/listings/{listing_id}", response_model=schemas.Listing)
def update_listing(listing_id: int, updated_listing: schemas.ListingCreate, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    for key, value in updated_listing.dict().items():
        setattr(listing, key, value)
    db.commit()
    db.refresh(listing)
    return listing

@app.delete("/listings/{listing_id}")
def delete_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    db.delete(listing)
    db.commit()
    return {"ok": True, "message": "Listing deleted"}
