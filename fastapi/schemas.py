from pydantic import BaseModel

class ListingBase(BaseModel):
    title: str
    society_name: str
    society_url: str
    posted_date: str
    rent_price: int
    description: str
    agent_name: str
    operating_since: str

class ListingCreate(ListingBase):
    pass

class Listing(ListingBase):
    id: int

    class Config:
        orm_mode = True
