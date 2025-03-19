import functools
from bin.services.db_service.user_service import check_food_record
from bin.response.response_model import ErrorResponseModel

def check_user_favourite_list(func):
    @functools.wraps(func)

    def wrapper(self,request, *args, **kwargs):
        data = check_food_record(request.user_id,request.food_id)
        if data:
            return ErrorResponseModel("This food already in favourite list", 400)
        return func(self,request,*args, **kwargs)
           
    return wrapper