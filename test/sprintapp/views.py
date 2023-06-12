from django.shortcuts import render,redirect
from .models import NutritionData,FoodData,User
from django.db.models import Q

def index(request) :
    return render(request,
                  "sprintapp/index.html",
                  {})
    # return HttpResponse("Oracle 페이지 입니다.")

def nutrition_data(request):
    data = NutritionData.objects.all()
    return render(request, 'sprintapp/nutrition_data.html', {'data': data})

def test(request) :
    return render(request,
                  "sprintapp/test.html",
                  {})

def food_data(request):
    data = FoodData.objects.all()
    return render(request, 'sprintapp/food_data.html', {'data': data})
    
def nutrition_data_view(request, age, gender):
    # age와 gender를 적절한 형식으로 변환
    input_age = int(age)
    input_gender = str(gender)

    age_ranges = [
        {'range': "20-29세", 'min': 20, 'max': 29},
        {'range': "30-39세", 'min': 30, 'max': 39},
        {'range': "40-49세", 'min': 40, 'max': 49},
        {'range': "50-59세", 'min': 50, 'max': 59},
        {'range': "60-69세", 'min': 60, 'max': 69},
        {'range': "70세 이상", 'min': 70, 'max': None},
    ]

    filtered_data = None

    for age_range in age_ranges:
        if age_range['max'] and age_range['min'] <= input_age <= age_range['max']:
            filtered_data = NutritionData.objects.filter(Q(age__startswith=str(age_range['min'])) | Q(age__startswith=str(age_range['max']))).filter(gender=input_gender)
            break
        elif age_range['max'] is None and age_range['min'] <= input_age:
            filtered_data = NutritionData.objects.filter(Q(age__startswith=str(age_range['min']))).filter(gender=input_gender)
            break

    if filtered_data.exists():
        # 데이터가 존재하는 경우
        data = filtered_data.first()
        calorie = data.calorie
        carbohydrates = data.carbohydrates
        protein = data.protein
        fat = data.fat
        sugar = data.sugar
        sodium = data.sodium

        return render(request, 'sprintapp/result.html', {
            'calorie': calorie,
            'carbohydrates': carbohydrates,
            'protein': protein,
            'fat': fat,
            'sugar': sugar,
            'sodium': sodium,
            'age': input_age,  # age 변수 추가
            'gender': input_gender  # gender 변수 추가
        })
    else:
        # 데이터가 존재하지 않는 경우
        return render(request, 'sprintapp/no_result.html')


def register_user(request):
    if request.method == 'POST':
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'sprintapp/error.html', {'message': '이미 존재하는 사용자입니다.'})

        latest_user = User.objects.order_by('-unique_id').first()
        latest_unique_id = latest_user.unique_id if latest_user else 0

        unique_id = latest_unique_id + 1

        user = User.objects.create(age=age, gender=gender, username=username, password=password, unique_id=unique_id)

        # nutrition_data_view로 age와 gender 값을 전달
        return redirect('nutrition_data_view', age=age, gender=gender)

    return render(request, 'sprintapp/form.html')