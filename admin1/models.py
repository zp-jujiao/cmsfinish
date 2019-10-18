from django.db import models
from datetime import datetime

#用户登录注册
class admin(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=8)
    email=models.CharField(max_length=50,null=True)
    lasttime=models.DateTimeField(null=True)
    headimg = models.CharField(max_length=50, null=True)
    userdetail= models.TextField(null=True)

    class Meta:
        db_table = "admin"

#文章分类（菜单）
class menu(models.Model):
    name=models.CharField(max_length=10)#菜单名
    class Meta:
        db_table = "menu"

#新闻列表
class news(models.Model):
    catid=models.IntegerField(max_length=11)
    title=models.CharField(max_length=30)
    title_font_color=models.CharField(max_length=10)#16进制的颜色标识
    thumb=models.CharField(max_length=30,null=True)
    num=models.IntegerField(max_length=11)
    registtime=models.DateTimeField(default=datetime.now())
    class Meta:
        db_table = "news"


#文章详情
class news_content(models.Model):
    newsid=models.IntegerField(max_length=11)
    content=models.TextField()
    class Meta:
        db_table = "news_content"

#文章推荐位分类
class position(models.Model):
    name=models.CharField(max_length=30)#推荐位名字
    class Meta:
        db_table = "position"


#存放不同推荐位下的文章id的
class position_content(models.Model):
    positionid=models.IntegerField(max_length=11)
    newsid=models.IntegerField(max_length=11)
    class Meta:
        db_table = "position_content"