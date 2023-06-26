from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.http import  JsonResponse
from .forms import PasswordLoginForm, SignUpForm
from .models import Foodinfo, Record, User, Standard, Photo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import date, timedelta
from django.db.models import Q,Sum
from .classifier import classify_image
from config import settings
import calendar
# Create your views here.

def soft(request):
    if request.method == 'POST':
        username = request.session['nickname'] 
        user = User.objects.get(nickname=username)    
        button_value = request.POST.get('button_value')
        # 결과 값을 템플릿에 전달하여 렌더링
        foodie = Foodinfo.objects.get(foodname=button_value)
        note = Record.objects.create(kcal = foodie.kcal,
                                     carbohydrate = foodie.carbohydrate,
                                     protein = foodie.protein,
                                     fat = foodie.fat,
                                     sugar = foodie.sugar,
                                     sodium = foodie.sodium,
                                     nickname = user)
        note.save()

        return JsonResponse({'redirect_url': '/user/menu/'})

def showresult(request):
    name = [
    "쌀밥",
    "미역국",
    "된장찌개",
    "돼지고기볶음",
    "마늘쫑무침",
    "숙주나물",
    "시금치나물",
    "김무침",
    "깍두기",
    "배추김치",
    "미역초무침",]

    food = []
    username = request.session['nickname'] 
    user = User.objects.get(nickname=username)
    proto = Photo.objects.filter(nickname=user).last()
    img_path = "C:/userapp" + proto.image.url
    classification = classify_image(img_path)
    for i in classification:
                food.append(name[int(i.numpy()[-1])])
    return render(request,
              "userapp/resultpage.html",
              {'proto' : proto, 'class' : food})

def upload(request):
    if request.method == 'POST' and request.FILES.get('image'):
        username = request.session.get('nickname')
        user = User.objects.get(nickname=username)
        image_file = request.FILES['image']
        photo = Photo.objects.create(image=image_file, nickname=user)
        photo.image = image_file
        photo.save()
        return JsonResponse({'message': '이미지 업로드 성공'}, status=200)
    else:
        return JsonResponse({'message': '이미지 업로드 실패'}, status=400)

def userindex(request):
    return render(request,
                  "userapp/userpage.html",
                  {})

def usermenu(request):
    nickname = request.session.get('nickname')
    return render(request,
                  "userapp/menupage.html",
                  {'nickname':nickname,})

def menucapture(request):
    return render(request,
                  "userapp/capturepage.html",
                  {})

def menudaily(request):
    user_info = get_user(request)
    nickname = request.session.get('nickname')
    today = date.today()

    records = Record.objects.filter(nickname__nickname=nickname, date=today)

    total_kcal = records.aggregate(Sum('kcal'))['kcal__sum']
    total_carbohydrate = records.aggregate(Sum('carbohydrate'))['carbohydrate__sum']
    total_protein = records.aggregate(Sum('protein'))['protein__sum']
    total_fat = records.aggregate(Sum('fat'))['fat__sum']
    total_sodium = records.aggregate(Sum('sodium'))['sodium__sum']
    total_sugar = records.aggregate(Sum('sugar'))['sugar__sum']
    return render(request,
                  "userapp/dailypage.html",
                  {'user_info': user_info,
                   'nickname':nickname,
                   'total_kcal': total_kcal,
                    'total_carbohydrate': total_carbohydrate,
                    'total_protein': total_protein,
                    'total_fat': total_fat,
                    'total_sodium': total_sodium,
                    'total_sugar': total_sugar,
                    'date': today,
                    })

def menuweekly(request):
    nickname = request.session.get('nickname')
    user_info = get_user(request)
    today = date.today()
    week_ago = today - timedelta(days=7)

    # 일주일간의 레코드 가져오기
    records = Record.objects.filter(
        nickname__nickname=nickname,
        date__range=[week_ago, today + timedelta(days=1)]  # 오늘을 포함한 7일 범위로 수정
    ).values('date').annotate(
        total_carbohydrate=Sum('carbohydrate'),
        total_protein=Sum('protein'),
        total_fat=Sum('fat'),
        total_sodium=Sum('sodium'),
        total_sugar=Sum('sugar')
    )

    # 영양 성분 차이 계산을 위한 초기값 설정
    max_difference = 0
    nutrient_with_max_difference = ''
    date_with_max_difference = None
    difference_sign = ''  # difference_sign 변수 초기화

    # 레코드 간의 영양 성분 차이 계산
    for record in records:
        difference = record['total_carbohydrate'] - user_info['carbohydrate_max']
        abs_difference = abs(difference) #절댓값 사용을 위해 abs 사용
        if abs_difference > max_difference:
            max_difference = abs_difference
            nutrient_with_max_difference = '탄수화물'
            date_with_max_difference = record['date']

            if difference > 0:
                difference_sign = '과다'
            else:
                difference_sign = '부족'

        difference = record['total_protein'] - user_info['protein_max']
        abs_difference = abs(difference)
        if abs_difference > max_difference:
            max_difference = abs_difference
            nutrient_with_max_difference = '단백질'
            date_with_max_difference = record['date']

            if difference > 0:
                difference_sign = '과다'
            else:
                difference_sign = '부족'

        difference = record['total_fat'] - user_info['fat_max']
        abs_difference = abs(difference)
        if abs_difference > max_difference:
            max_difference = abs_difference
            nutrient_with_max_difference = '지방'
            date_with_max_difference = record['date']

            if difference > 0:
                difference_sign = '과다'
            else:
                difference_sign = '부족'

        difference = record['total_sodium'] - user_info['sodium']
        abs_difference = abs(difference)
        if abs_difference > max_difference:
            max_difference = abs_difference
            nutrient_with_max_difference = '나트륨'
            date_with_max_difference = record['date']

            if difference > 0:
                difference_sign = '과다'
            else:
                difference_sign = '부족'

        difference = record['total_sugar'] - user_info['sugar']
        abs_difference = abs(difference)
        if abs_difference > max_difference:
            max_difference = abs_difference
            nutrient_with_max_difference = '당류'
            date_with_max_difference = record['date']

            if difference > 0:
                difference_sign = '과다'
            else:
                difference_sign = '부족'

    # 요일 정보 가져오기
    if date_with_max_difference:
        day_of_week = calendar.day_name[date_with_max_difference.weekday()]
        # 요일을 한국어로 변환
        day_of_week = {
            'Monday': '월요일',
            'Tuesday': '화요일',
            'Wednesday': '수요일',
            'Thursday': '목요일',
            'Friday': '금요일',
            'Saturday': '토요일',
            'Sunday': '일요일'
        }.get(day_of_week, '')  # 요일이 없는 경우 빈 문자열로 설정
    else:
        day_of_week = ''

    return render(request, "userapp/weeklypage.html", {
        'user_info': user_info,
        'nickname': nickname,
        'nutrient_max': nutrient_with_max_difference,  # 가장 차이나는 영양성분
        'difference_sign': difference_sign,  # 부족인지 과다인지 표현
        'date_with_max_difference': date_with_max_difference,  # 가장 큰 차이값이 나타난 날짜
        'day_of_week': day_of_week,  # 해당하는 요일
    })

def usersignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 세션 초기화 및 닉네임 저장
            request.session.flush()
            request.session['nickname'] = user.nickname
            return redirect('/user/menu/')  # 회원가입 후 리다이렉트할 URL
    else:
        form = SignUpForm()
    return render(request, 'userapp/signuppage.html', {'form': form})

def userlogin(request):
    if request.method == 'POST':
        form = PasswordLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = str(form.cleaned_data['password'])
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # 세션 초기화 및 닉네임 저장
                request.session.flush()
                request.session['nickname'] = user.nickname
                return redirect('/user/menu/')  # 로그인 성공 후 리디렉션할 URL
            else:
                form.add_error('password', '올바른 아이디와 비밀번호를 입력하세요.')
    else:
        form = PasswordLoginForm()

    return render(request, 'userapp/loginpage.html', {'form': form})

def search_food(request):
    query = request.GET.get('query')
    if query:
        results = Foodinfo.objects.filter(foodname__icontains=query)
    else:
        results = Foodinfo.objects.all()

    # 페이징 처리
    paginator = Paginator(results, 10) 
    page = request.GET.get('page')  # 현재 페이지 번호를 가져옴

    try:
        foods = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우, 첫 페이지를 보여줌
        foods = paginator.page(1)
    except EmptyPage:
        # 페이지 번호가 유효하지 않은 경우, 마지막 페이지를 보여줌
        foods = paginator.page(paginator.num_pages)

    selected_foods = request.GET.get('selected_foods')
    if selected_foods:
        selected_food_ids = list(map(int, selected_foods.split(',')))
    else:
        selected_food_ids = []

    context = {
        'foods': foods,
        'selected_food_ids': selected_food_ids,
    }
    return render(request, 'userapp/search_food.html', context)

def select_foods(request):
    if request.method == 'GET':
        select_food_ids = request.GET.get('selected_food_ids')
        if select_food_ids:
            select_food_ids = select_food_ids.split(",")
            selected_foods = Foodinfo.objects.filter(id__in=select_food_ids)
        else:
            selected_foods = []
        
        context = {
            'selected_foods': selected_foods
        }
        
        return render(request, 'userapp/select_foods.html', context)
    
    else:
        return HttpResponse('Invalid request')
    
def save_foods(request):
    tableset = [0,0,0,0,0,0]
    
    if request.method == 'GET':
        username = request.session['nickname'] 
        user = User.objects.get(nickname=username)
        select_food_ids = request.GET.get('selected_foods')
        if select_food_ids:
            select_food_ids = select_food_ids.split(",")
            selected_foods = Foodinfo.objects.filter(id__in=select_food_ids)
        else:
            selected_foods = []
        
        for i in selected_foods:
            tableset[0] += i.kcal 
            tableset[1] += i.carbohydrate 
            tableset[2] += i.protein 
            tableset[3] += i.fat 
            tableset[4] += i.sugar 
            tableset[5] += i.sodium
    
        u = Record.objects.create(nickname=user,kcal=tableset[0],
                                carbohydrate=tableset[1],protein=tableset[2],
                                fat=tableset[3],sugar=tableset[4],sodium=tableset[5])
        u.save()    
        return render(request,'userapp/menupage.html',{'nickname' : username})
    
    else:
        return HttpResponse('Invalid request')

def get_user(request):
    today = date.today()
    nickname = request.session.get('nickname', None)
    if nickname:
        try:
            user = User.objects.get(nickname=nickname)
            age = today.year - user.birth
            gender = '남성' if user.gender == 'male' else '여성'
            standard = Standard.objects.get(
                Q(age_min__lte=age) & Q(age_max__gte=age),
                gender=gender
            )

            return {
                'kcal_min': standard.kcal_min,
                'kcal_max': standard.kcal_max,
                'carbohydrate_min': standard.carbohydrate_min,
                'carbohydrate_max': standard.carbohydrate_max,
                'protein_min': standard.protein_min,
                'protein_max': standard.protein_max,
                'fat_min': standard.fat_min,
                'fat_max': standard.fat_max,
                'sodium': standard.sodium,
                'sugar': standard.sugar
            }
        except User.DoesNotExist:
            return None
        except Standard.DoesNotExist:
            return None
    else:
        return None
    
def dailypage(request):
    user_info = get_user(request)
    return render(request, "userapp/dailypage.html", {'user_info': user_info})


