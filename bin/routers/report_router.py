import json
import re
from PIL import Image
import io
from fastapi import FastAPI,APIRouter,Query,Depends,UploadFile, File
from fastapi.exceptions import HTTPException
import google.generativeai as genai
from bin.requests.report_request import AllUserData,FilterReportData
from bin.controllers.report_controller import reportManager
from bin.controllers.food_image_controller import parse_nutrition_response

genai.configure(api_key="AIzaSyASeQiLE6cjeJnPA7it1yd2EHI40fZ1u68")

model = genai.GenerativeModel('gemini-1.5-flash')

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

@router.post('/import-csv')
async def import_csv_file(file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    else:
        return await reportManager.csv_file(file)
    
@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Validate file type (basic check)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # Read the image bytes
    contents = await file.read()

    try:
        # Open image using PIL
        image = Image.open(io.BytesIO(contents))
        prompt = """
            This is a food image. Identify the food item, list its main ingredients, and estimate the nutritional information per serving.

            Return your result **strictly as a JSON object** with the following structure:

            {
            "food": "string",
            "ingredients": ["string", "string", ...],
            "estimated_nutrition_per_serving": {
                "calories": "string",
                "fat": "string",
                "saturated_fat": "string",
                "cholesterol": "string",
                "sodium": "string",
                "carbohydrates": "string",
                "fiber": "string",
                "sugar": "string",
                "protein": "string"
            }
            }

            Only return the JSON. Do not include any explanation or markdown formatting.
            """

        response = model.generate_content([prompt, image])
        print('resposne test--->',response.text)
        raw_text = response.text.strip()
        clean_text = re.sub(r"^```json\s*|\s*```$", "", raw_text, flags=re.DOTALL).strip()
        result_json = json.loads(clean_text)
        # result = parse_nutrition_response(response.text)
        return {"result": result_json}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")