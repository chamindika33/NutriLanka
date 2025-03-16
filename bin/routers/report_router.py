from fastapi import FastAPI,APIRouter,Query,Depends
from fastapi.exceptions import HTTPException
from bin.requests.report_request import AllUserData,FilterReportData
from bin.controllers.report_controller import reportManager

router = APIRouter(
    prefix="/nutri-lanka",
    tags=["Report"]
)


@router.post('/get-all-users')
def all_users(request:AllUserData):
    return reportManager.get_all_user_list(request)

@router.post('/get-all-users-dietary-data')
def get_all_users_dietary_data(request:AllUserData):
    return reportManager.get_all_dietary_list(request)

@router.post('/get-dietary-report-filter')
async def get_user_dietary_report_filter(request:FilterReportData):
    return reportManager.filter_dietary_data(request)