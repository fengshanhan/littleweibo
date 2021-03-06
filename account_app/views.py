# from django.http import HttpResponse
from django.shortcuts import render, redirect  # 返回网页需要import的包
from django.contrib.auth import authenticate, login as loginfunc, logout as logoutfunc  # 从授权app导入模块
from django.contrib.auth.backends import ModelBackend  # 修改验证模块
from django.db.models import Q
from django.contrib.auth.decorators import login_required  #装饰器： 必须登录后才访问
import re
from .forms import RegistrationForm,PasswordUpdateForm,  EmailUpdateForm,ReleaseForm,LikeForm
from .models import User
from account_app import models
import datetime
import time
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
                request.session['useremail'] = e0.email # session存的email
            else:
                request.session['useremail'] = username
            return redirect('account_app:home')

        else:
            e = None
            e = User.objects.filter(username=username)
            if e:
                return render(request, 'account_app/login.html', {'error': "illegal password."})
            else:
                e2 = None
                e2 = User.objects.filter(email=username)
                if e2:
                    return render(request, 'account_app/login.html', {'error': "illegal password."})
                else:
                    pattern = re.compile(r"\"?([-a-z0-9.`?{}]+@\w+\.\w+)\"?")
                    if re.match(pattern, username):
                        return render(request, 'account_app/login.html', {'error': "Email not exist."})
                    else:
                        return render(request, 'account_app/login.html', {'error': "Username not exist."})


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
            return redirect('account_app:login')
        else:
            return render(request, 'account_app/register.html', {'form': form})
    else:
        return render(request, 'account_app/register.html')
"""
@login_required
def like(request,like):
    if request.method=='POST':
        ee = User.objects.filter(email=request.session['useremail'])  # 获取user表中含有的点赞者的数据
        username2 = ee[0].username  # 首先获得点赞者username
        weiboId = request.POST['weiboId']#从前端获取微博号
        e = like.objects.filter(userName2=username2,weiboId=weiboId)  # 获取like表中取出该用户点赞的该微博号的一条记录
        u0 = e[0]  # fetch第一行数据
        username1 = u0.userName1  # 被点赞者username
        obj = models.weibo.object.create(userName1=username1, userName2=username2, weiboId=weiboId,time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        obj.save()#将点赞人，被点赞人，点赞微博，点赞时间存入数据库
        m = weibo.objects.get(weiboId=weiboId) #从weibo表中取出该微博ID号的记录进行更改
        e0=m[5]#取出该微博的点赞数
        e0=e0+1
        m.likeNum=e0
        m.save()
        weibos = models.weibo.objects.all().order_by('-weiboDate')
        your_like = 'your like is :{like}'.format(like=like)
        return render(request,your_like, {'weibos': weibos})
    return render(request, 'account_app/home.html')
"""

"""@login_required
def notlike(request,notlike):
    if request.method=='POST':

        ee = User.objects.filter(username=request.session['useremail'])  # 获取user表中含有的点赞者的数据
        username2 = ee[0].username  # 首先获得点赞者username
        weiboId = request.POST['weiboId']  # 从前端获取微博号

        models.like.filter(weiboId=weiboId,userName2=username2).delete()#在like表中删除点赞的这条记录
        e = weibo.objects.get(weiboId=weiboId)#获取weibo表中该微博的记录
        e0 = e[5]  # 取出该微博的点赞数
        e0 = e0 - 1 #点赞数减1
        e.likeNum = e0
        e.save()
        weibos = models.weibo.objects.all().order_by('-weiboDate')
        your_notlike='your notlike is :{notlike}'.format(notlike=notlike)
        return render(request, your_notlike, {'weibos': weibos})
    return render(request, 'account_app/home.html')
"""

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
    if request.method=='POST':
        weiboId = request.POST['weiboId']  # 从前端获取微博号

        if "view" in request.POST:
            print("now in views")
            # 获取当前微博的所有评论并返回
            comments = models.Comment.objects.filter(weiboId=weiboId)
            print("comments:")
            print(comments)
            weibo=models.weibo.objects.filter(weiboId=weiboId)
            e = User.objects.filter(email=request.session['useremail'])
            e0 = e[0]  # fetch第一行数据
            img = User.objects.filter(username=e0.username)
            weibos = models.weibo.objects.all().order_by('-weiboDate')
            return render(request,'account_app/comments.html',{'weibo':weibo,'img':img,'comments':comments})

        elif "like" in request.POST:
            print("now in like")
            ee = User.objects.filter(email=request.session['useremail'])  # 获取当前用户信息
            print("username")
            username = ee[0].username  # 首先获得点赞者username

            print(username)
            print(weiboId)
            try:

                e = models.like.objects.get(userName=username,weiboId=weiboId)  # 获取like表中取出该用户点赞的该微博号的一条记录

                if e.state == 1:
                    e.state = 0
                    e.save()
                    m = models.weibo.objects.get(weiboId=weiboId)  # 从weibo表中取出该微博ID号的记录进行更改
                    print(m.content)
                    e0 = m.likeNum  # 取出该微博的点赞数
                    e0 = e0 - 1
                    m.likeNum = e0
                    m.save()
                elif e.state == 0:
                    e.state = 1
                    print("!!!!!")
                    e.save()
                    m = models.weibo.objects.get(weiboId=weiboId)  # 从weibo表中取出该微博ID号的记录进行更改
                    e0 = m.likeNum  # 取出该微博的点赞数
                    e0 = e0 + 1
                    m.likeNum = e0
                    m.save()
            except Exception as e:
                #不存在点赞记录
                obj = models.like.objects.create(weiboId=weiboId,userName=username,state=1)
                obj.save()
                m = models.weibo.objects.get(weiboId=weiboId) #从weibo表中取出该微博ID号的记录进行更改
                e0=m.likeNum#取出该微博的点赞数
                e0=e0+1
                m.likeNum=e0
                m.save()

        elif "comment" in request.POST:
            print("now in comments")
            weiboId = request.POST['weiboId']  # 从前端获取微博号
            comment = request.POST['comments']
            ee = User.objects.filter(email=request.session['useremail'])  # 获取当前用户信息
            #print("username")
            username = ee[0].username  # 首先获得评论者username
            obj=models.Comment.objects.create(weiboId=weiboId,userName=username,comContent=comment,comDate= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),comGood=0)
            obj.save()

            m = models.weibo.objects.get(weiboId=weiboId)  # 从weibo表中取出该微博ID号的记录进行更改
            e0 = m.commentNum  # 取出该微博的点赞数
            e0 = e0 + 1
            m.commentNum = e0
            m.save()


    e = User.objects.filter(email=request.session['useremail'])
    e0 = e[0]  # fetch第一行数据
    img = User.objects.filter(username=e0.username)
    weibos = models.weibo.objects.all().order_by('-weiboDate')
    return render(request, 'account_app/home.html', {'weibos': weibos,'img':img})

def comments(request):
    return render(request, 'account_app/comments.html')

# 发布微博页
@login_required
def release(request):
    if request.method == 'POST':
        content = request.POST['content']
        user = User.objects.filter(email=request.session['useremail'])
        u0 = user[0]  # fetch第一行数据
        u00=u0.username
        obj = models.weibo.objects.create(userName=u00, content=content,weiboDate= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),state=0)
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
    # 获取头像
    e = User.objects.filter(email=request.session['useremail'])
    e0 = e[0]  # fetch第一行数据
    img = User.objects.filter(username=e0.username)
    # 获取头像完毕
    return render(request, 'account_app/personal.html',{'img':img})

'''
#微博广场
def weiboHome(request):
    username=models.weibo.userName
    datetime=models.weibo.weiboDate
'''