from fastapi import FastAPI,APIRouter,Query
from fastapi.exceptions import HTTPException
from bin.requests.user_request import NewUser
from bin.controllers.user_controller import userManager

router = APIRouter(
    prefix="/nutri-lanka",
    tags="User"
)

@router.post("/create-user")
async def create_new_user(request:NewUser):
    return await userManager.create_user(request)