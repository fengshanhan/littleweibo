from django.db import models

from django.contrib.auth.models import AbstractUser

from django.conf import settings
from uuid import uuid4
import os


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False



# 让上传的文件路径动态地与user的名字有关，即上传路径为 media/headshot/username/filename
def upload_to(instance, filename):
    #上传的图片都会以随机的uuid字符串命名
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join("../media/headshot",instance.username, filename)

# Create your models here.
# 用户信息
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, null=False) # 用户名
    email = models.EmailField(unique=True, null=False) # 邮箱
    created_at = models.DateField(auto_now_add=True)  # 注册日期，自动创建---永远是创建时的时间， 插入时不需要这个字段
    # 上传图像必须要安装Pillow库，如果没安装运行pip install Pillow安装
    # upload_to='upload'表示用户上传数据存储的位置，这里需要注意：在数据库中实际保存的并不是文件，而是文件存放的路径
    headshot = models.ImageField(upload_to = upload_to, default='../media/head.png', blank=True, null=True) # 头像，创建初始默认为head.png
    fansNum = models.IntegerField(default=0, null=False) # 粉丝数量，创建初始默认为0
    concernsNum = models.IntegerField(default=0, null=False) # 关注数量，创建初始默认为0
    weiboNum = models.IntegerField(default=0, null=False) # 微博数量，创建初始默认为0
    description = models.TextField(default='',null=True, blank=True) # 个人简介，创建初始默认为空


# 让上传的文件路径动态地与weiboid有关，即上传路径为 media/weibo/weiboid/filename
def upload_to2(instance, filename):
    # 上传的图片都会以随机的uuid字符串命名
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join("../media/weibo", instance.weiboId, filename)

# 每条微博信息
class weibo(models.Model):
    weiboId = models.AutoField(primary_key= True) # 微博id， 自增列
    userName = models.CharField(max_length=30, null=False) # 用户名
    content = models.TextField(max_length=300,null=False, blank=False) # 微博内容， 限制300， 不允许为空
    weiboDate = models.DateTimeField(auto_now_add=True) # 发布日期，自动创建---永远是创建时的时间， 插入时不需要这个字段
    commentNum = models.IntegerField(default=0, null=False) # 评论数，创建初始默认为0
    likeNum = models.IntegerField(default=0, null=False) # 点赞数，创建初始默认为0
    transmitNum = models.IntegerField(default=0, null=False) # 转发数，创建初始默认为0
    state = models.IntegerField(null=False) # 是否转发， 0：自己发的 1：转发的
    transmitCon = models.TextField(null=True, blank=True) # 转发评论的内容， 允许为空
    # upload_to='upload'表示用户上传数据存储的位置，这里需要注意：在数据库中实际保存的并不是文件，而是文件存放的路径
    image = models.ImageField(upload_to = upload_to2)

# 评论信息
class Comment(models.Model):
    weiboId = models.IntegerField(null=False) # 所评论的微博id
    userName1 = models.CharField(max_length=30, null=False) # 被评论的用户名
    userName2 = models.CharField(max_length=30)  # 评论的用户名
    comContent = models.TextField(null=False, blank=False) # 评论内容， 不允许为空
    comDate = models.DateTimeField(auto_now_add=True) # 评论发布日期，自动创建---永远是创建时的时间， 插入时不需要这个字段
    comGood= models.IntegerField(default=0, null=False) # 评论获得的点赞数，创建初始默认为0

#关注信息
class follow(models.Model):
    userName = models.CharField(max_length=30, null=False) # 用户名， 被关注的人
    fansName = models.CharField(max_length=30, null=False) # 粉丝名， 关注的人
    time = models.DateTimeField(auto_now_add=True)  # 关注时间

#点赞信息
class like(models.Model):
    weiboId = models.IntegerField(null=False)  # 所点赞的微博id
    userName1 = models.CharField(max_length=30, null=False)  # 被点赞的用户名
    userName2 = models.CharField(max_length=30)  # 点赞的用户名#当前登陆者
    time=models.DateTimeField(auto_now_add=True)#点赞时间





