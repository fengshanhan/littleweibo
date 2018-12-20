from django.urls import path
from . import views  # 导入views

from django.conf.urls.static import static
from django.conf import settings


app_name = 'account_app'
urlpatterns = [
    path('', views.land, name="land"),  # landing page
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/',views.register, name='register'),
    path('me/', views.me, name='me'),
    path('profile/', views.profile, name='profile'),

    path('home/', views.home,name='home'), # 微博主页
    path('home/<comment>/',views.comment,name='comment'), # 微博主页
    path('home/<like>/', views.like,name='like'), # 微博主页
    path('home/<notlike>/',views.notlike,name='notlike'), # 微博主页

    path('release/', views.release, name='release'), # 发布微博
    path('personal/', views.personal, name='personal'), # 个人主页
    path('personal/changeHeadshot', views.changeHeadshot, name='changeHeadshot'),  # 个人主页

    path('RecentNews/', views.RecentNews, name='RecentNews'), # 消息
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  这句话是用来指定和映射静态文件的路径
