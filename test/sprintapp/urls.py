from django.urls import path
from . import views

urlpatterns = [
    ### http://127.0.0.1:8000/sprint/
    path('', views.index),
    ### http://127.0.0.1:8000/sprint/index/
    path('index/', views.index),

    ### http://127.0.0.1:8000/sprint/test/
    path('test/', views.test),

    path('nutrition_data/', views.nutrition_data, name='nutrition_data'),

    path('food_data/', views.food_data, name='food_data'),

    path('nutrition/<int:age>/<str:gender>/', views.nutrition_data_view, name='nutrition_data_view'),
    
    path('register_user/', views.register_user, name='register_user'),
]