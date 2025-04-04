from fastapi import FastAPI,APIRouter,Query,Depends
from fastapi.exceptions import HTTPException
from bin.requests.user_request import NewUser,UserLoginRequest,AddFavoriteItem,SetDieatGoals,SetDailyLimit,AvatarUpdateRequest,AddCustomRecipe,CustomRecipe
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
    return userManager.add_food_record_to_favorite_list(request,authentication)

@router.get('/get-user-favourite-list')
def get_user_favourite_list(user_id:str, authentication=Depends(Authorization())):
    return userManager.get_user_favourite_food_list(user_id,authentication)

@router.post('/set-dieatary-goal')
def set_dieatary_goal(request:SetDieatGoals,authentication=Depends(Authorization())):
    return userManager.set_user_dietary_goal(request,authentication)

@router.put('/update-daily-limit')
def update_daily_limit(request:SetDailyLimit,authentication=Depends(Authorization())):
    return userManager.update_user_daily_limit(request,authentication)

@router.get('/get-user-daily-limit')
def get_user_daily_limit(user_id:str,authentication=Depends(Authorization())):
    return userManager.get_user_daily_dieatary_limit(user_id,authentication)

@router.put('/image')
async def update_profile_image(request: AvatarUpdateRequest, authentication=Depends(Authorization())):
    return userManager.update_user_img(request=request, auth=authentication)

@router.get('/image')
async def get_profile_image(authentication=Depends(Authorization())):
    return userManager.get_user_img(auth=authentication)

@router.post('/add-custom-recipes')
def add_custom_recipes(request:AddCustomRecipe, authentication=Depends(Authorization())):
    return userManager.add_user_custom_recipe(request,authentication)

@router.get('/get-user-custom-recipes')
async def get_user_custom_recipes(authentication=Depends(Authorization())):
    return userManager.get_custom_recipe(auth=authentication)

@router.get('/get-user-details')
async def get_user_details(authentication=Depends(Authorization())):
    return userManager.send_user_details(auth=authentication)

@router.post('/new-custom-recipes')
def new_custom_recipes(request:CustomRecipe, authentication=Depends(Authorization())):
    return userManager.user_custom_recipe(request,authentication)
