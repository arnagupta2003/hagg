from sqlalchemy import Column, Integer, String
from database import Base

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    society_name = Column(String)
    society_url = Column(String)
    posted_date = Column(String)
    rent_price = Column(String)
    description = Column(String)
    agent_name = Column(String)
    operating_since = Column(String)
