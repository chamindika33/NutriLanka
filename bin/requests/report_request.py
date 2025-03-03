from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

class AllUserData(BaseModel):
    page_number : int
    record_per_page : int