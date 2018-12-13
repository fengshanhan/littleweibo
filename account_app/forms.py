from django import forms
import re
from django.contrib.auth.backends import ModelBackend  # 修改验证模块
from django.db.models import Q
from .models import User


# 重写验证函数，让用户可以用邮箱登录
# setting 里要有对应的配置
class CustomBackend(ModelBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        try:
            # user = User.objects.get(Q(username=username) | Q(email=username)) #既可以邮箱也可以用户名登录
            user = User.objects.get(Q(email=email))  #只能邮箱登录
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class RegistrationForm(forms.Form):

    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField(label='Email',)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,required=True)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput,required=True)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        pattern = re.compile('^.[a-z]+$')
        if not re.match(pattern, username):
            raise forms.ValidationError("username has illegal characters.")
        existuser = User.objects.filter(username=username)
        if existuser:
            raise forms.ValidationError("username already taken.")
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
        if not re.match(pattern, email):
            raise forms.ValidationError("enter a valid email address.")
        existuser = User.objects.filter(email=email)
        if existuser:
            raise forms.ValidationError("email already taken.")
        else:
            return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("password too short.")
        else:
            return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("password mismatch.")
        else:
            return password2


class LoginForm(forms.Form):

    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existuser = User.objects.filter(email=email)
        try:
            existuser = User.objects.get(email=email)
        except User.DoesNotExist:
            existuser = None
        if not existuser:
            raise forms.ValidationError("email not found.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        if password is None:
            raise forms.ValidationError("password is invalid.")
        existuser = User.objects.filter(email=email)
        authentication = CustomBackend()
        auth_user = authentication.authenticate(email=email, password=password)  # 验证user

        if existuser:
            if not auth_user:
                raise forms.ValidationError("password is invalid.")

        return password


class PasswordUpdateForm(forms.Form):
    oldpassword = forms.CharField(label='Old Password')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Password Confirmation')

    def clean_password1(self):#验证新密码是否正确
        oldpassword = self.cleaned_data.get('oldpassword')
        if oldpassword is None:
            raise forms.ValidationError("password is invalid.")
        return oldpassword


    def clean_password1(self):#验证新密码是否正确
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("password too short.")
        else:
            return password1

    def clean_password2(self):#验证密码与密码是否一致
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("password mismatch.")
        else:
            return password2


class EmailUpdateForm(forms.Form):
    new_email = forms.EmailField(label='New Email')

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
        if not re.match(pattern, new_email):
            raise forms.ValidationError("enter a valid email address.")
        try:
            existuser = User.objects.get(email=new_email)
        except User.DoesNotExist:
            existuser = None
        if existuser:
            raise forms.ValidationError("email already taken.")
        else:
            return new_email