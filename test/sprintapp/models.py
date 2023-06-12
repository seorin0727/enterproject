from django.db import models

# Create your models here.
class NutritionData(models.Model):
    age = models.CharField(max_length=20, null=False)
    gender = models.CharField(max_length=20, null=False)
    calorie = models.CharField(max_length=20, null=False)
    carbohydrates = models.CharField(max_length=20, null=False)
    protein = models.CharField(max_length=20, null=False)
    fat = models.CharField(max_length=20, null=False)
    sugar = models.CharField(max_length=20, null=False)
    sodium = models.CharField(max_length=20, null=False)


class FoodData(models.Model): 
    name = models.CharField(max_length=20, null=False)
    weight = models.CharField(max_length=20, null=False)
    calorie = models.CharField(max_length=20, null=False)
    carbohydrates = models.CharField(max_length=20, null=False)
    protein = models.CharField(max_length=20, null=False)
    fat = models.CharField(max_length=20, null=False)
    sugar = models.CharField(max_length=20, null=False)
    sodium = models.CharField(max_length=20, null=False)


class User(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    unique_id = models.IntegerField()

    # 추가 필드가 있다면 여기에 정의할 수 있습니다.

    def __str__(self):
        return self.username