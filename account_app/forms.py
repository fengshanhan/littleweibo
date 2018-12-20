from django import forms
import re
from .models import User

class RegistrationForm(forms.Form):

    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField(label='Email',)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,required=True)
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput,required=True)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        pattern = re.compile('^.[a-zA-Z0-9_-]+$')
        if not re.match(pattern, username):
            raise forms.ValidationError("username has illegal characters.")
        existuser = User.objects.filter(username=username)
        if existuser:
            raise forms.ValidationError("username already taken.")
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        pattern = re.compile(r"\"?([-a-z0-9.`?{}]+@\w+\.\w+)\"?")
        if not re.match(pattern, email):
            raise forms.ValidationError("enter a valid email address.Concern that email must be lowercase")
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



class PasswordUpdateForm(forms.Form):
    oldpassword = forms.CharField(label='OldPassword')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Confirm')

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
        pattern = re.compile(r"\"?([-a-z0-9.`?{}]+@\w+\.\w+)\"?")
        if not re.match(pattern, new_email):
            raise forms.ValidationError("enter a valid email address.Concern that email must be lowercase")
        try:
            existuser = User.objects.get(email=new_email)
        except User.DoesNotExist:
            existuser = None
        if existuser:
            raise forms.ValidationError("email already taken.")
        else:
            return new_email

class ReleaseForm(forms.Form):
    content = forms.CharField(label='content')
    at = forms.CharField(label='at')

    # def clean_content(self):
    #     content = self.cleaned_data.get('content')
    #     if len(content)<1 or len(content)>300:
    #         raise forms.ValidationError("Content length incorrect!")
    #     return content
    # def clean_at(self):
    #     at = self.cleaned_data.get('at')
    #     return at

class LikeForm(forms.Form):
    weiboId=forms.IntegerField(label='weiboId')
    userName = forms.CharField(label='userName') #当前用户ID
    state = forms.IntegerField(label='state')

class CommentForm(forms.Form):
    weiboId = forms.IntegerField(label='weiboId')  # 所评论的微博id
    userName = forms.CharField(label='userName')  # 评论的用户名
    comContent = forms.CharField(label='comContent')  # 评论内容， 不允许为空
    comDate = forms.DateTimeField(label='comDate')  # 评论发布日期，自动创建---永远是创建时的时间， 插入时不需要这个字段
    comGood = forms.IntegerField(label='comGood')  # 评论获得的点赞数，创建初始默认为0
