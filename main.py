import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = 76
HEIGHT_CM = 183
AGE = 21

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
BEARER_HEADERS = {
    "Authorization": os.environ.get("TOKEN")
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ.get("SHEET_ENDPOINT")

exercise_text = input("Tell me which exercises you did: ")

parameters = {

     "query": exercise_text,
     "gender": GENDER,
     "weight_kg": WEIGHT_KG,
     "height_cm": HEIGHT_CM,
     "age": AGE,

}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)


today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=BEARER_HEADERS)

print(sheet_response.text)


