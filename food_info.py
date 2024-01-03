import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()
import os
food_info_key= os.getenv('SPOONACULAR_API_KEY_FOOD_INFO')


# app = Flask(__name__)
# @app.route('/')
# def get_food_query():
#     return render_template("index.html")

# @app.route('/search',methods=["GET","POST"])
def get_food_info(food_query):
    # food_query=request.form["query"]
    image_api_params = {
        "query": food_query,
        "apiKey":food_info_key
    }
    image_response = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=image_api_params)
    image_url = image_response.json().get("results")[0]["image"]
    info_response = requests.get(f"https://api.spoonacular.com/recipes/guessNutrition?title={food_query}",
                                 params=image_api_params)
    info_data = info_response.json()
    calories_content = info_data.get("calories").get("value")
    fats_content = info_data.get("fat").get("value")
    carbs_content = info_data.get("carbs").get("value")
    protien_content = info_data.get("protein").get("value")
    food_data_list = [food_query.upper(), image_url, calories_content, protien_content, carbs_content, fats_content]
    return (food_data_list)

