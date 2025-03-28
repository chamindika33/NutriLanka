from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

class AllUserData(BaseModel):
    page_number : int
    record_per_page : int

class FilterReportData(BaseModel):
    filter_name: str
    status: bool
    page_number : int
    record_per_page : int


class ImageBase64Request(BaseModel):
    base64_image: str 

