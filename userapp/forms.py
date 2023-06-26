from django import forms
# from django.contrib.auth.forms import AuthenticationForm
from .models import User, Record

class PasswordLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'font-weight: bold;', 'placeholder': '여기 눌러 별명 입력'}))
    password = forms.CharField(label="", widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'font-weight: bold;', 'placeholder': '여기 눌러 비밀번호 입력'}))


class SignUpForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('female', '여성'),
        ('male', '남성'),
    ]
    nickname = forms.CharField(label="", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'font-weight: bold;', 'placeholder': '여기 눌러 별명 입력'}))
    gender = forms.ChoiceField(label="성별",choices=GENDER_CHOICES,widget=forms.RadioSelect(attrs={'class': 'form-control',}))
    password = forms.CharField(label="", widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'font-weight: bold;', 'placeholder': '여기 눌러 비밀번호 입력'}))
    birth = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'font-weight: bold;', 'placeholder': '여기 눌러 생년 입력'}))

    class Meta:
        model = User
        fields = ['nickname','password', 'birth', 'gender']  # 추가 필드들도 포함

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class InsertForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['kcal','carbohydrate','protein','fat','sodium','sugar',
                'nickname']
        # labels = {}

    def save(self, commit=True):
        diet = super().save(commit=False)
        if commit:
            diet.save()
        return diet