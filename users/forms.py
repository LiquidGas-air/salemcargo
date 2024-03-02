from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Parcel
from django.core.exceptions import ValidationError
from .models import UserProfile

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['track_code', 'description']



class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Логин уже используется.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email уже используется.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) < 10:
            raise ValidationError("Phone number must be exactly 10 digits long.")
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Данный номер уже используется.")
        return phone_number
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if len(password1) < 8:
            raise ValidationError("Пароль должен состоять как минимум из 8 символов.")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password1

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user