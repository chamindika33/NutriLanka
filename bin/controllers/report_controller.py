from fastapi import HTTPException
from bin.response.response_model import ResponseModel,ErrorResponseModel
from bin.services.db_service.report_service import get_all_users,get_all_users_dietary_list,get_filtered_dietary_list


class ReportManager():
    def get_all_user_list(self,request):
        try:
            offset = (request.page_number-1) * request.record_per_page
            print('offset-->', offset)
            data = get_all_users(offset,request.record_per_page)
            result ={
                'data': data['data'],
                'page_number': request.page_number,
                'record_per_page': request.record_per_page,
                'No of records': data['total_records']
            }

            return ResponseModel(result, "retrieved data")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def get_all_dietary_list(self,request):
        try:
            offset = (request.page_number-1) * request.record_per_page
            print('offset-->', offset)
            data = get_all_users_dietary_list(offset,request.record_per_page)
            result ={
                'data': data['data'],
                'page_number': request.page_number,
                'record_per_page': request.record_per_page,
                'No of records': data['total_records']
            }

            return ResponseModel(result, "retrieved data")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def filter_dietary_data(self,request):
        try:
            offset = (request.page_number-1) * request.record_per_page
            print('offset-->', offset)
            data = get_filtered_dietary_list(offset,request.record_per_page,request.filter_name,request.status)
            result ={
                'data': data['data'],
                'page_number': request.page_number,
                'record_per_page': request.record_per_page,
                'No of records': data['total_records']
            }

            return ResponseModel(result, "retrieved data")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
        
        
reportManager = ReportManager()