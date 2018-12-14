# from django.http import HttpResponse
from django.shortcuts import render, redirect  # 返回网页需要import的包
from django.contrib.auth import authenticate, login as loginfunc, logout as logoutfunc  # 从授权app导入模块
from django.contrib.auth.backends import ModelBackend  # 修改验证模块
from django.db.models import Q
from django.contrib.auth.decorators import login_required  #装饰器： 必须登录后才访问

from .forms import RegistrationForm,PasswordUpdateForm, EmailUpdateForm,ReleaseForm
from .models import User
from .models import weibo
from account_app import models
import datetime
# 重写验证函数，让用户可以用邮箱登录
# setting 里要有对应的配置
class CustomBackend(ModelBackend):
    def authenticate(self,  username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username)) #既可以邮箱也可以用户名登录
            #user = User.objects.get(Q(email=email))  #只能邮箱登录
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# landing page
def land(request):
    if request.user.is_authenticated:  # 如果是登录状态
        return redirect("account_app:home")
    #return redirect("account_app:login")
    return render(request, "account_app/land.html")


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        authentication = CustomBackend()
        user = authentication.authenticate(username=username, password=password) #y验证user
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 给user手动添加backend
            loginfunc(request, user)# 重命名登录函数

            e = None
            e = User.objects.filter(username=username)
            if e:
                e0 = e[0]
                request.session['useremail'] = e0.email
            else:
                request.session['useremail'] = username

            return redirect('account_app:home')  # 重定向的函数
        else:
            return render(request, 'account_app/login.html', {'error': "username or password has error"})

    else:
        return render(request, 'account_app/login.html')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            # 添加到数据库
            # 必须使用objects.create_user()函数来创建对象才能加密密码,密码是加密保存而不是明文，用了这个不需要user.save()
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('/login')
        else:
            return render(request, 'account_app/register.html', {'form': form})
    else:
        return render(request, 'account_app/register.html')


@login_required
def me(request):
    # filter作用相当于sql语句的select，在这里是select--- where email=值
    e = User.objects.filter(email=request.session['useremail'])
    e0 = e[0]  # fetch第一行数据
    return render(request, 'account_app/me.html', {'user': e0})


@login_required
def logout(request):
    del request.session['useremail']
    logoutfunc(request)  # 登出
    return redirect("account_app:login") #重定向函数


@login_required
def profile(request):
    e = User.objects.filter(email=request.session['useremail'])
    e0 = e[0]  # fetch第一行数据
    if request.method == 'POST':
        if request.POST.get('password1', ""):
            form = PasswordUpdateForm(request.POST)
            if form.is_valid():
                oldpassword = form.cleaned_data['oldpassword']
                password = form.cleaned_data['password1']
                user = User.objects.get(email=request.session["useremail"])
                if user.check_password(oldpassword):
                    user.set_password(password)
                    user.save()
                    return redirect("account_app:login")
                else:
                    data = 'invalid password.'
                    return render(request, 'account_app/profile.html', {'data': data, 'user': e0})
            else:
                return render(request, 'account_app/profile.html', {'form': form, 'user': e0})
        else:
            form = EmailUpdateForm(request.POST)
            if form.is_valid():
                new_email = form.cleaned_data['new_email']
                user = User.objects.get(username=request.user.username)
                user.email = new_email
                user.save()
                return redirect("account_app:login")
            return render(request, 'account_app/profile.html', {'form': form, 'user': e0})

    return render(request, 'account_app/profile.html', {'user': e0})

# 主页
def home(request):
    weibos = models.weibo.objects.all().order_by('-weiboDate')
    return render(request, 'account_app/home.html', {'weibos': weibos})

# 发布微博页
@login_required
def release(request):
    if request.method == 'POST':
        content = request.POST['content']
        obj = models.weibo.objects.create(userName='zzxz', content=content, state=0)
        obj.save()
        return redirect("account_app:home")


        '''
        
        form = ReleaseForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            at = form.cleaned_data['at']
            image = request.FILES.get('img')
            weiboDate = datetime.datetime.now().strftime('%Y-%m-%d');
            obj = models.weibo.objects.create(weiboId='4328',userName='zzxz',content=content,
                                              weiboDate=weiboDate,commentNum=0,likeNum=0,transmitNum=0,
                                              state=0,transmitCon=at,image=image)
            obj.save()
            return render(request, 'account_app/release.html')
        else:
            return redirect("account_app:message")
        
        
        '''

    return render(request, 'account_app/release.html')

# 消息页
@login_required
def message(request):
    return render(request, 'account_app/message.html')

# 个人主页
@login_required
def personal(request):
    return render(request, 'account_app/personal.html')

#微博广场
def weiboHome(request):
    username=models.weibo.userName
    datetime=models.weibo.weiboDate