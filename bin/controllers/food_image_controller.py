import re

def parse_nutrition_response(response_text: str) -> dict:
    # Extract food name
    food_match = re.search(r"That's a \*\*(.+?)\*\*", response_text)
    food_name = food_match.group(1) if food_match else "Unknown"

    # Extract ingredients
    ingredients = re.findall(r"\*\*(.*?)\*\*:", response_text)

    # Nutrition data block
    nutrition_matches = {
        "calories": re.search(r"Calories:\s*([\d\-–]+.*)", response_text),
        "fat": re.search(r"Fat:\s*([\d\-–]+.*)", response_text),
        "saturated_fat": re.search(r"Saturated Fat:\s*([\d\-–]+.*)", response_text),
        "cholesterol": re.search(r"Cholesterol:\s*([\d\-–]+.*)", response_text),
        "sodium": re.search(r"Sodium:\s*([\d\-–]+.*)", response_text),
        "carbohydrates": re.search(r"Carbohydrates:\s*([\d\-–]+.*)", response_text),
        "fiber": re.search(r"Fiber:\s*([\d\-–]+.*)", response_text),
        "sugar": re.search(r"Sugar:\s*([\d\-–]+.*)", response_text),
        "protein": re.search(r"Protein:\s*([\d\-–]+.*)", response_text),
    }

    nutrition_data = {
        k: v.group(1).strip() if v else "N/A"
        for k, v in nutrition_matches.items()
    }

    return {
        "food": food_name,
        "ingredients": ingredients,
        "estimated_nutrition_per_serving": nutrition_data
    }


