from django.shortcuts import  render
from django.contrib import messages
from datetime import date
from .models import User, CaloriesPerDay
import requests
import json

def index(request):
    if "submit" in request.POST:
        name = request.POST.get("name")
        food = request.POST.get("food")
        grams = request.POST.get("grams")
        url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"
        querystring = {"query":f"{grams}g {food}"}
        headers = {
            'x-rapidapi-host': "nutrition-by-api-ninjas.p.rapidapi.com",
            'x-rapidapi-key': "b5a8a5938fmsh2c8b21bff24ef3fp1a064ajsn51ba5a865d45"
        }
        response_API = requests.request("GET", url, headers=headers, params=querystring)
        data = response_API.text
        parse_json = json.loads(data)
        request.session["name"] = name

        if not User.objects.filter(name=name.lower()):
            messages.error(request, "No user with this name!")
        else:
            if not len(parse_json) == 0:
                all_data = parse_json[0]
                food_name = parse_json[0]["name"]
                calories = parse_json[0]["calories"]
                serving_size = parse_json[0]["serving_size_g"]
                fat = parse_json[0]["fat_total_g"]
                fat_saturated = parse_json[0]["fat_saturated_g"]
                protein = parse_json[0]["protein_g"]
                cholesterol = parse_json[0]["cholesterol_mg"]
                fiber = parse_json[0]["fiber_g"]
                sugar = parse_json[0]["sugar_g"]
                carbs = parse_json[0]["carbohydrates_total_g"]

                context = {
                    "all_data": all_data,
                    "food_name": food_name,
                    "calories": calories,
                    "serving_size": serving_size,
                    "fat": fat,
                    "fat_saturated": fat_saturated,
                    "protein": protein,
                    "cholesterol": cholesterol,
                    "fiber": fiber,
                    "sugar": sugar,
                    "carbs": carbs,
                    }

                request.session["calories"] = calories
            else:
                messages.error(request, "No food detected!")
            return render(request, "home.html", context)

    if "apply" in request.POST:

        user_from_input = User.objects.filter(name=request.session["name"].lower())[0]
        query_list = CaloriesPerDay.objects.all()

        for item in query_list:
            if str(item) == f'{request.session["name"].lower()}-{date.today()}':
                user_today_calories = CaloriesPerDay.objects.get(user_name=user_from_input, day=date.today()).day_bmr
                user_today_calories = int(user_today_calories) + int(request.session["calories"])
                CaloriesPerDay.objects.filter(user_name=user_from_input, day=date.today()).update(day_bmr=int(user_today_calories))

        if CaloriesPerDay.objects.filter(user_name=user_from_input, day=date.today()).count() == 0:
            CaloriesPerDay.objects.create(user_name=user_from_input, day_bmr=int(request.session["calories"]))
                
        total_day_calories = User.objects.get(name=request.session["name"].lower()).bmr
        today_calories = CaloriesPerDay.objects.get(user_name=user_from_input, day=date.today()).day_bmr
        percentage = int(today_calories) // (int(total_day_calories) // 100)
        if percentage > 100:
            percentage_bar_color = "progress-bar progress-bar-striped bg-danger"
        else:
            percentage_bar_color = "progress-bar progress-bar-striped"

        context_v2 = {
            "total_day_calories": total_day_calories, 
            "today_calories":   today_calories, 
            "percentage": percentage,
            "percentage_bar_color": percentage_bar_color
            }

        del request.session['name']
        del request.session['calories']

        return render(request, "home.html", context_v2)
    return render(request, "home.html")


def bmr_calculator(request):
    if "submit" in request.POST:
        print("jo")
        name = request.POST.get("name")
        weight = request.POST.get("weight")
        height = request.POST.get("height")
        age = request.POST.get("age")
        gender = request.POST.get("radio_button")
        activity = request.POST.get("select_field")
        print(name, weight, height, age, gender, activity)
        if not User.objects.filter(name=name):
            if gender == "men":
                BMR = (10*int(weight) + 6.25*int(height) - 5*int(age) + 5) * float(activity.split("+")[0])
            else:
                BMR = (10*int(weight) + 6.25*int(height) - 5*int(age) -161) * float(activity.split("+")[0])
            context = {
                "name": name,
                "bmr": int(BMR),
                "weight": weight,
                "height": height,
                "age": age,
                "gender": gender,
                "activity": activity.split("+")[1]
            }
            User.objects.create(name=name.lower(), weight=weight, 
                height=height, age=age, gender=gender, activity=activity.split("+")[1], bmr=int(BMR))
            return render(request, "bmr.html", context)
        else:
            messages.error(request, "Name is already taken!")
    return render(request, "bmr.html")
