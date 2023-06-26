from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, nickname, password, **extra_fields):
        if not nickname:
            raise ValueError('The Nickname field must be set')
        if not password:
            raise ValueError('The PhoneNumber field must be set')
        user = self.model(nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nickname, password, **extra_fields)

    def create_superuser(self, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(nickname, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()
    # password = models.IntegerField(max_length=4)
    birth = models.IntegerField(max_length=4)
    gender = models.CharField(max_length=20) 
    nickname = models.CharField(max_length=20, primary_key=True)
    email = None
    username = None
    first_name = None
    last_name = None
    last_login = None
    date_joined = None
    is_staff = None
    
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['gender', 'birth']

    def __str__(self):
        return self.nickname


class Record(models.Model):
    kcal = models.IntegerField()
    carbohydrate = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
    sugar = models.IntegerField()
    date = models.DateField(auto_now=True)
    nickname = models.ForeignKey("User",on_delete=models.CASCADE, db_column="nickname")

class Foodinfo(models.Model):
    foodname = models.CharField(max_length=20)
    kcal = models.FloatField()
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    sodium = models.FloatField()
    sugar = models.FloatField()

class Standard(models.Model):
    age_min = models.IntegerField()
    age_max = models.IntegerField()
    gender = models.CharField(max_length=20) 
    kcal_min = models.IntegerField()
    kcal_max = models.IntegerField()
    carbohydrate_min = models.IntegerField()
    carbohydrate_max = models.IntegerField()
    protein_min = models.IntegerField()
    protein_max = models.IntegerField()
    fat_min = models.IntegerField()
    fat_max = models.IntegerField()
    sodium = models.IntegerField()
    sugar = models.IntegerField()

class Photo(models.Model):
    nickname = models.ForeignKey("User",on_delete=models.CASCADE, db_column="nickname")
    image = models.ImageField(upload_to='images/')