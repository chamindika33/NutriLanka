import csv
import io
import json
from fastapi import HTTPException
from types import SimpleNamespace
from bin.services.db_service.food_service import create_new_food_record2
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


    async def csv_file(self,file):
        content = await file.read()
        decoded = content.decode('utf-8')
        io_string = io.StringIO(decoded)
        reader = csv.DictReader(io_string)

        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        records_created = 0
        for row in reader:
            try:
                print('row-->',row)
                row = {k.strip(): v.strip() for k, v in row.items() if k}
                # Convert numeric fields
                float_fields = ['calories', 'protein', 'carbohydrates', 'water', 'fat', 'vitamins', 'fiber',
                                'calcium', 'magnesium', 'phosphorus', 'sodium', 'potassium', 'iron', 'zinc',
                                'selenium', 'copper', 'manganese']
                for field in float_fields:
                    row[field] = float(row.get(field, 0) or 0)

                # Parse ingredients field if it's JSON-like string
                raw_ingredients = row.get('ingredients', '').strip()
                ingredients = json.loads(raw_ingredients if raw_ingredients else '[]')

                class RequestObject:
                    pass
                req = RequestObject()
                for key in row:
                    setattr(req, key, row[key])

                req = SimpleNamespace(**row)  
                await create_new_food_record2(req, ingredients, image_data=None)
                records_created += 1


            except Exception as e:
                print(f"Error processing row: {e}")
                continue

        return {"status": "success", "records_created": records_created}
       

        
        
        
reportManager = ReportManager()