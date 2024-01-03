from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from nutrition_management import Nutrients_manager
import bcrypt
import datetime
from recipe_manager import search_csv
from news import get_all_posts
from food_info import get_food_info

app = Flask(__name__)
nutrients_manager = Nutrients_manager()

# app.config['MONGO_DBNAME'] = "NUTRIVERSE"
app.config['MONGO_URI'] = "mongodb://localhost:27017/NUTRIVERSE"

mongo = PyMongo(app)


# global is_logged_in
# is_logged_in = False
@app.route("/")
def landing_page():
    if session.get('user_id') != None:
        is_logged_in = True
    else:
        is_logged_in = False
    return render_template("landing-page.html", is_logged_in=is_logged_in)


@app.route('/welcome')
def welcome():
    if session.get('user_id') != None:
        is_logged_in = True
        email = session['user_id']
        users = mongo.db.users
        filter = {
            "email": email
        }
        user = users.find_one(filter=filter)
        gender = user.get('gender')
        user_nutri_track_data = users.find_one(filter=filter).get('nutrients_tracker')
        if user_nutri_track_data is None:
            return render_template("welcome_dashboard.html",
                                name=user['name'], email=email,
                                gender_file_name=gender.lower(),
                                total_daily_data=None,
                                last_30_days_data=None,
                                goal=None )
        date = str(datetime.datetime.now().date())
        goal = users.find_one(filter=filter).get('goal')
        total_daily_data = {'name': '',
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
                            'time': ""
                            }
        for added_food in user_nutri_track_data:
            if str(added_food['time']).startswith(date):
                added_food.pop('time')
                # total_daily_data =  {key: total_daily_data[f'{key}'] + added_food[f'{key}'] if type(key) != str else added_food['name'] + ' ' + total_daily_data['name'] for key in added_food}
                total_daily_data = {
                    key: total_daily_data[f'{key}'] + round(added_food[f'{key}']) if key != 'name' else added_food['name'] + ' and ' + total_daily_data['name'] for key in added_food}

        if gender == None or gender == "Prefer Not to Say":
            gender = "demo"
        return render_template(
                                "welcome_dashboard.html",
                                name=user['name'], email=email,
                                gender_file_name=gender.lower(), 
                                total_daily_data=total_daily_data,
                                last_30_days_data=get_last_30_days_data(users.find_one(filter=filter).get('nutrients_tracker'), date),
                                goal=goal
                            )
    else:
        is_logged_in = False
        return render_template("required_login.html")


@app.route("/welcome/add_food", methods=["POST"])
def add_food():
    email = session['user_id']
    query = request.form['foodInput']
    hour = datetime.datetime.now().hour
    today = datetime.datetime.now().date()
    today = "2023-11-13"
    total_intake = nutrients_manager.get_nutrients_from_query_raw(query=query)
    # add_food_button_function(user_id=email, date=today, hour=hour, food_items=total_intake )
    add_food_button_funtion_raw(user_id=email, added_intake=total_intake)
    return redirect(url_for('welcome'))


@app.route("/edit_goals", methods=["GET", "POST"])
def edit_goals():
    if request.method == "GET":
        if session['user_id'] != None:
            return render_template('goal_form.html')
        else:
            return render_template("required_login.html")
    elif request.method == "POST":
        calories = request.form["calories"]
        proteins = request.form["proteins"]
        carbs = request.form["carbs"]
        fats = request.form["fats"]
        goal = {
            "calories": calories,
            "proteins": proteins,
            "carbs": carbs,
            "fats": fats
        }
        users = mongo.db.users
        email = session['user_id']
        users.update_one(filter={"email": email}, update={
            "$set": {
                "goal": goal
            }
        })
        return redirect(url_for('welcome'))


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        users = mongo.db.users
        entered_name = request.form['name']
        entered_email = request.form['email']
        entered_gender = request.form['gender']
        existing_user = users.find_one({'email': entered_email})

        if existing_user is None:
            hashpass = request.form['password']
            users.insert_one(
                {'name': entered_name, 'email': entered_email, 'gender': entered_gender, 'password': hashpass})
            session['user_id'] = entered_email
            # return "User Logged in successfully."
            return redirect(url_for('welcome'))
        return "User Already Present"
    return render_template('sign_up.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})
        if login_user != None:
            if request.form['password'] == login_user['password']:
                session['user_id'] = login_user['email']
                return redirect(url_for('welcome'))
            render_template("login_failed.html")
        return render_template("login_failed.html")


@app.route('/logout_user')
def logout():
    session['user_id'] = None
    return redirect(url_for('landing_page'))


''' ******  Search Recipe section  *******'''


@app.route('/recipes')
def recipe_search():
    if session['user_id'] != None:
        return render_template('recipe_form.html')
    else:
        return render_template("required_login.html")


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    recipe_details_dict = search_csv('NutriVerse WebApp/data/food_recipes.csv', 'recipe_title', query, 'recipe_title',
                                     max_results=10)
    for recipe in recipe_details_dict:
        # recipe["ingredients"]=recipe["ingredients"].replace("|",",")
        recipe["instructions"] = recipe["instructions"].replace('|', '').replace('. ', '.\n')

    return render_template('display_recipes_results.html', results=recipe_details_dict)


''' ******  Read Blogs section  *******'''


@app.route('/blogs')
def read_blogs():
    return render_template('blogs.html', all_posts=get_all_posts())


''' Nutrients Facts Section'''


@app.route("/food_info")
def food_info():
    return render_template("nutri_info_facts.html")


@app.route("/food_info/food", methods=["POST"])
def show_food_info():
    food_query = request.form["query"]
    return render_template("food_info_results.html", food_data=get_food_info(food_query=food_query))


def get_user_details_from_database(user_session_email):
    users = mongo.db.users
    logged_in_user = users.find_one({'email': user_session_email})
    return logged_in_user


def add_food_button_function(user_id, date, hour, food_items):
    users = mongo.db.users
    for food_item in food_items:
        # Update the document in MongoDB using the $push operator
        result = users.update_one(
            {
                "email": user_id,
            },
            {
                "$set": {
                    f"nutrients_tracker.daily_intake.{date}.hourly_intake.{hour}": food_item
                }
            }
        )
    filter = {'email': user_id}
    user_nutri_track_data = users.find_one(filter=filter).get('nutrients_tracker')
    update_total_hourly_data(filter=filter, date=date, user_nutri_track_data=user_nutri_track_data, hour=hour)
    user_nutri_track_data = users.find_one(filter=filter).get('nutrients_tracker')
    update_daily_data(filter=filter, date=date, user_nutri_track_data=user_nutri_track_data)


def add_food_button_funtion_raw(user_id, added_intake):
    users = mongo.db.users

    result = users.update_one(
        {
            "email": user_id,
        },
        {
            "$push": {
                f"nutrients_tracker": added_intake
            }
        }
    )


def update_daily_data(filter, date, user_nutri_track_data):
    daily_list = user_nutri_track_data.get('daily_intake').get(f"{date}").get('hourly_intake')
    dishes_ate = []
    total_calories = 0
    total_fats = 0
    total_proteins = 0
    total_carbs = 0

    hourly_totals = {key: value for key, value in daily_list.items() if key.startswith('hourly_total_')}
    for key, value in hourly_totals.items():
        total_calories += value["calories"]
        total_fats += value["fats"]
        total_proteins += value["proteins"]
        total_carbs += value["carbs"]
        dishes_ate.extend(value["names"])

    total = {
        "names": dishes_ate,
        "calories": total_calories,
        "fats": total_fats,
        "proteins": total_proteins,
        "carbs": total_carbs
    }
    users = mongo.db.users
    users.update_one(
        filter,
        {"$set": {
            f"nutrients_tracker.daily_intake.{date}.daily_total_{date}": total
        }
        }
    )


def update_total_hourly_data(filter, date, user_nutri_track_data, hour):
    hourly_list = [user_nutri_track_data.get('daily_intake').get(f"{date}").get('hourly_intake').get(f"{hour}")]
    dishes_ate = []
    total_calories = 0
    total_fats = 0
    total_proteins = 0
    total_carbs = 0
    if hourly_list != None:
        for foodset in hourly_list:
            dishes_ate.append(foodset['name'])
            total_calories += foodset['calories']
            total_fats += foodset['fats']
            total_proteins += foodset['proteins']
            total_carbs += foodset['carbs']
    total = {
        "names": dishes_ate,
        "calories": total_calories,
        "fats": total_fats,
        "proteins": total_proteins,
        "carbs": total_carbs
    }
    users = mongo.db.users
    users.update_one(
        filter,
        {"$set": {
            f"nutrients_tracker.daily_intake.{date}.hourly_intake.hourly_total_{hour}": total
        }
        }
    )


def get_last_30_days_data(user_nutri_track_data: list, date):
    # group each food by day
    last_30_days_data_dict = {

    }
    for nutrient in ["calories", "protein_g", "carbohydrates_total_g", "fat_total_g"]:
        total = 0
        protein_list = []
        date = user_nutri_track_data[-1]['time'].date()
        for record in list(reversed(user_nutri_track_data)):

            if date == record['time'].date():
                total = total + record[f"{nutrient}"]
            else:
                protein_list.append(total)
                total = 0
                date = record['time'].date()
        protein_list.append(total)

        last_30_days_data_dict[f"{nutrient}_last_30_days"] = protein_list
        if nutrient == "calories":
            protein_list = [round(num / 10) for num in protein_list]
            last_30_days_data_dict[f"{nutrient}_last_30_days"] = protein_list

    print(last_30_days_data_dict)
    # only last 30 days
    # create array
    return last_30_days_data_dict


if __name__ == "__main__":
    app.secret_key = "secretkeyagain"
    app.run(debug=True)
