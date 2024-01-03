from dataclasses import dataclass
import requests
import datetime
import pprint
import os
from dotenv import load_dotenv
load_dotenv()

my_api_key=os.getenv("NUTRITION_API_KEY")

@dataclass
class Food:
    name:str
    calories: int
    proteins: int
    fat: int 
    carbohydrates: int

class Nutrients_manager:
    def __init__(self) -> None:
        self.today = []   #get todays data from database

    def get_nutrients_from_query(self, query):
        # now = datetime.datetime.now()
        # current_hour = now.hour

        headers={
                "X-Api-Key": my_api_key,
            }       
        response=requests.get(f"https://api.api-ninjas.com/v1/nutrition?query={query}", headers=headers)
        data=response.json()
        food_list = []
        for dish in data:
            nutrients_data = {
                    "name" : dish["name"],
                    "calories":dish["calories"],
                    "fats":dish["fat_total_g"],
                    "proteins":dish["protein_g"],
                    "carbs":dish["carbohydrates_total_g"]
                }
            food_list.append(nutrients_data)
        return food_list
    
    def get_nutrients_from_query_raw(self, query):
        now = datetime.datetime.now()
        current_hour = now.hour

        headers={
                "X-Api-Key": my_api_key
            }       
        response=requests.get(f"https://api.api-ninjas.com/v1/nutrition?query={query}", headers=headers)
        data=response.json()
        final_result_intake_dict = {'name':'',
                                    'calories': 0, 
                                    'serving_size_g': 0, 
                                    'fat_total_g': 0, 
                                    'fat_saturated_g': 0, 
                                    'protein_g': 0, 
                                    'sodium_mg': 0, 
                                    'potassium_mg': 0, 
                                    'cholesterol_mg': 0, 
                                    'carbohydrates_total_g': 0, 
                                    'fiber_g': 0, 
                                    'sugar_g': 0,
        }
        for dict_dish in data:
            # final_result_intake_dict = {key: final_result_intake_dict[f'{key}'] + dict_dish[f'{key}'] for key in dict_dish}
            final_result_intake_dict = {key: final_result_intake_dict[f'{key}'] + round(dict_dish[f'{key}']) if key != 'name' else dict_dish['name'] + ' ' + final_result_intake_dict['name'] for key in dict_dish}

        final_result_intake_dict['time'] = now
        return final_result_intake_dict
    
# nut = Nutrients_manager()
# print(nut.get_nutrients_from_query_raw("rice pakoda"))
