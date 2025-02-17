from fastapi import FastAPI,APIRouter,Query,Depends
from fastapi.exceptions import HTTPException
from bin.requests.user_request import NewUser,UserLoginRequest,AddFavoriteItem
from bin.middleware.user_middleware import Authorization
from bin.services.custom_validations import check_user_email
from bin.controllers.user_controller import userManager

router = APIRouter(
    prefix="/nutri-lanka",
    tags=["User"]
)

@router.post("/create-user")
async def create_new_user(request:NewUser):
    if await check_user_email(request.email):
        raise HTTPException(status_code=400, detail="This email is already in use")
    else:
        return await userManager.create_user(request)
    
@router.post('/login')
def sign_in_user(request: UserLoginRequest):
    return userManager.sign_in(request)

@router.post('/add-food-to-favorite-list')
def add_food_to_favorite_list(request:AddFavoriteItem, authentication=Depends(Authorization())):
    return userManager.add_food_record_to_favorite_list(request,auth=authentication)

@router.get('/get-user-favourite-list')
def get_user_favourite_list(user_id:str, authentication=Depends(Authorization())):
    return userManager.get_user_favourite_food_list(user_id,auth=authentication)