from django.template import loader
from django.shortcuts import render, redirect, HttpResponse
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
from admin1.models import *
from common import utils
from cmsfinish import settings
from datetime import datetime
import math
import os
import json
import re

currentAdmin=""  #当前登录用户
class TestUEditorForm(forms.Form):
    content = UEditorField('', width=500, height=200, toolbars="full", imagePath="static/images/", filePath="static/files/",upload_settings={"imageMaxSize":1204000},settings={})

# 用户管理
def userlist(request):
    # 搜索title关键字  初始值为空
    keyword = ""
    if request.GET.get("keyword"):
        keyword = request.GET.get("keyword")
    print(keyword)
    # 分页   首先判断当前有没有页数  设定默认值为第一页
    page = 1
    if request.GET.get("page"):
        page = int(request.GET.get("page"))

    # 当前总页数向上取整
    allPage = math.ceil(admin.objects.filter(username__contains=keyword).count() / 2)
    print("页数", allPage)
    startIndex = 2 * (int(page) - 1)
    endIndex = 2 * int(page)
    # 调用方法
    ret = utils.setpage(allPage, page)
    userList = admin.objects.filter(username__contains=keyword).order_by('-lasttime')[
                   startIndex:endIndex]

    # 菜单列表
    # 将页码存进列表中
    print("我是总页数--------", allPage)
    allPageList = range(ret[0], ret[1])
    positionName = position.objects.all()
    context = {
        "userList":userList,
        "currentAdmin": currentAdmin,
        "allPageList": allPageList,
        "page": page,
        "keyword":keyword,
        "allPage": allPage
    }
    return render(request,"admin/admin/adminList.html",context)

#添加管理员
def addUser(request):
    template=loader.get_template('admin/admin/addUser.html')
    form = TestUEditorForm()
    context = {"form": form,"currentAdmin": currentAdmin}
    return HttpResponse(template.render(context, request))
#添加管理员处理
def addUserHandler(request):
    headImg = request.FILES.get("headimg")
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get("email")
    content = request.POST.get('content')
    print(username,password,email)
    # 按照用户名进行判断
    userinfo=admin.objects.filter(username=username)
    if userinfo:
        # 不为空时提示该用户名已存在
        return HttpResponse(utils.returnResult(1, "用户名已存在，请重新添加"))
        # 为空时判断缩略图是否为空
    if headImg:
        # 不为空的时候
        imgSize = utils.getsize(headImg.size, settings.UPLOADS["unit"])
        if headImg.name.split(".")[len(headImg.name.split(".")) - 1] not in settings.UPLOADS["types"]:
            return HttpResponse(utils.returnResult(1, "文件类型不正确"))
        if float(imgSize) > settings.UPLOADS["maxsize"]:
            return HttpResponse(utils.returnResult(1, "文件过大"))
        filename = "newsImg" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split("/")[-1]
        # 对文件是否存在进行判断
        dir = "static/uploads"
        utils.confirmImgFile(dir)
        imgpath = dir + "/" + filename
        with open(imgpath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
        admin(username=username, password=password, headImg=filename,userdetail=content,email=email).save()
        return HttpResponse(utils.returnResult(0, "添加管理员成功"))
    admin(username=username, password=password,userdetail=content,email=email).save()
    return HttpResponse(utils.returnResult(0, "添加管理员成功"))

# 管理员编辑
def editUser(request):
    template = loader.get_template('admin/admin/editUser.html')
    form = TestUEditorForm()
    id = request.GET.get("id")
    userList=admin.objects.filter(id=id).all()
    print(id)
    context = {
        "form": form,
        "currentAdmin": currentAdmin,
        "userList":userList[0]
    }
    return HttpResponse(template.render(context, request))

#管理员编辑处理
def editUserHandler(request):
    id== request.FILES.get("id")
    headImg = request.FILES.get("headimg")
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get("email")
    content = request.POST.get('content')
    print(username, password, email)
    if headImg:
        # 不为空的时候
        imgSize = utils.getsize(headImg.size, settings.UPLOADS["unit"])
        if headImg.name.split(".")[len(headImg.name.split(".")) - 1] not in settings.UPLOADS["types"]:
            return HttpResponse(utils.returnResult(1, "文件类型不正确"))
        if float(imgSize) > settings.UPLOADS["maxsize"]:
            return HttpResponse(utils.returnResult(1, "文件过大"))
        filename = "newsImg" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split("/")[-1]
        # 对文件是否存在进行判断
        dir = "static/uploads"
        utils.confirmImgFile(dir)
        imgpath = dir + "/" + filename
        with open(imgpath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
                #   删除废弃图片
        preImg = request.POST.get("preImg")
        print("删除", preImg)
        path1 = 'static/uploads' + preImg
        path = os.path.join(settings.BASE_DIR, path1)
        os.remove(path)
        print("删除成功")
        #   更新数据库
        admin.objects.filter(id=id).update(username=username, password=password, headImg=filename, userdetail=content, email=email)
        return HttpResponse(utils.returnResult(0, "管理员修改成功"))
    admin.objects.filter(id=id).update(username=username, password=password, userdetail=content, email=email)
    return HttpResponse(utils.returnResult(0, "管理员修改成功"))

#管理员管理
# def index(request):
#     return render(request, "admin/index.html")

# 登录界面渲染
def login(request):
    template=loader.get_template('admin/login.html')
    context = {}
    return HttpResponse(template.render(context,request))

# 登录页面处理
def loginHandler(request):
    # 接收前端提交的数据
    username = request.POST.get("username")
    password = request.POST.get("password")
    userinfo = admin.objects.values("password").filter(username=username)
    print(username+"===="+password)
    if userinfo.count()>0:
        #  当用户名存在的时候
        if password == userinfo[0]["password"]:
            admin.objects.filter(username=username).update(lasttime=datetime.now())
            request.session['admin'] = username
            return HttpResponse(utils.returnResult(0, "登录成功,欢迎来到路赞后台管理系统") )
        #     return JsonResponse(utils.returnResult(0, "登录成功,欢迎来到路赞后台管理系统"))
        return HttpResponse(utils.returnResult(1, "密码输入错误,请重新输入"))
    else:
        return HttpResponse(utils.returnResult(1, "用户名输入错误,请再次确认"))


# 退出登录界面
def loginout(request):
    # 删除session中缓存的数据
    request.session.flush()
    print("删除成功")
    # 重定向到登录界面
    return redirect("/admin/login")

# 首页
def homePage(request):
    template = loader.get_template('admin/homePage.html')
    # 当前登录用户
    global currentAdmin
    currentAdmin=  request.session['admin']
    # 登陆用户数量
    today=datetime.now().strftime("%y-%m-%d")
    userSum=admin.objects.filter(lasttime__contains=today).count()
    # 文章数量
    newsSum=news.objects.filter().count()
    # 获取推荐位数量
    positionSum = position.objects.filter().count()
    # 最大阅读数
    maxNum = news.objects.values("num").order_by("-num")[0:1]
    context = {
        "currentAdmin": currentAdmin,
        "userSum":userSum,
        "newsSum":newsSum,
        "positionSum":positionSum,
        "maxNum":maxNum[0]["num"]
    }
    return HttpResponse(template.render(context, request))

# 菜单管理页面
def menuList(request):
    template=loader.get_template('admin/menu/menuList.html')
    # option 搜索  获取id
    catid=-1
    if request.GET.get("id"):
        catid=int(request.GET.get("id"))
    print("我是id",catid)
    # 分页   首先判断当前有没有页数  设定默认值为第一页
    page=1
    if request.GET.get("page"):
        page=int(request.GET.get("page"))
    print(request.GET.get("page"))
    # 当前总页数向上取整
    if catid==-1:
        allPage = math.ceil(menu.objects.all().count()/2)
    else:
        allPage = math.ceil(menu.objects.filter(id=catid).count()/2)
    print("----------------------------",allPage)
    startIndex = 2 * (int(page) - 1)
    endIndex = 2 * int(page)
    ret=utils.setpage(allPage,page)
    print("---",startIndex,endIndex)
    if catid == -1:
        menuList=menu.objects.all()[startIndex:endIndex]
    else:
        menuList=menu.objects.filter(id=catid)[startIndex:endIndex]
    allPageList=range(ret[0],ret[1])
    #     注入下拉菜单
    menuListOption = menu.objects.all()
    listinfo=[]
    for item in menuList:
        listinfo.append(item)
    context = {
        "listinfo":listinfo,
        "currentAdmin":currentAdmin,
        "allPageList":allPageList,
        "page":page,
        "catid":catid,
        "menuListOption":menuListOption,
        "allPage":allPage
    }
    return HttpResponse(template.render(context,request))

# 添加菜单
def addMenu(request):
    template=loader.get_template('admin/menu/addMenu.html')
    context = {"currentAdmin":currentAdmin}
    return HttpResponse(template.render(context,request))

# 添加菜单处理
def addMenuHandler(request):
    # 获取前端传递过来的数据存储到数据库
    menuname = request.POST.get('menuname')
    classify = request.POST.get('classify')
    status=request.POST.get('status')
    menuType=request.POST.get('menuType')
    menuinfo = menu.objects.filter(name=menuname).all()
    # 判断当前菜单名是否
    if menuinfo:
        return HttpResponse(utils.returnResult(1, "该菜单名已存在，请重新添加"))
    else:
        menu(name=menuname,status=status,menuType=menuType,classify=classify).save()
        return HttpResponse(utils.returnResult(0, "菜单添加成功"))

# 删除菜单
def delMenuHandler(request):
    menusid = request.GET.get("menusid")
    print(menusid)
    try:
        menu.objects.filter(id=menusid).delete()
        return HttpResponse(utils.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(utils.returnResult(1, "删除失败"))

# 编辑菜单
def editMenu(request):
    template = loader.get_template('admin/menu/editMenu.html')
    id = request.GET.get('id')
    print("编辑",id)
    menuInfo=menu.objects.filter(id=id)
    menInfoList=[]
    for list in menuInfo:
        menInfoList=list
    context = {
        "currentAdmin": currentAdmin,
        "menInfoList":menInfoList
    }
    return HttpResponse(template.render(context, request))

# 编辑菜单处理
def editMenuHandler(request):
    # 获取前端传递过来的数据存储到数据库
    id=request.POST.get('menuid')
    menuname = request.POST.get('menuname')
    classify = request.POST.get('classify')
    status = request.POST.get('status')
    menuType = request.POST.get('menuType')
    print("我是信息",id,status,menuType,menuname,classify)
    try:
        menu.objects.filter(id=id).update(name=menuname,status=status,menuType=menuType,classify=classify)
        return HttpResponse(utils.returnResult(0, "修改菜单成功"))
    except Exception as e:
        return HttpResponse(utils.returnResult(0, "修改菜单失败"))

# 新闻列表
def newsList(request):
    template = loader.get_template('admin/news/newsList.html')
    # option 搜索  获取id
    catid = -1
    if request.GET.get("catid"):
        catid = int(request.GET.get("catid"))
    print("我是catid",catid)
    # 搜索title关键字  初始值为空
    searchTitle = ""
    if request.GET.get("searchTitle"):
        searchTitle = request.GET.get("searchTitle")

    print("搜索",searchTitle)
    # 分页   首先判断当前有没有页数  设定默认值为第一页
    page = 1
    if request.GET.get("page"):
        page = int(request.GET.get("page"))
    # 当前总页数向上取整
    if catid == -1:
        allPage = math.ceil(news.objects.filter(title__contains=searchTitle).count() / 2)
    else:
        allPage = math.ceil(news.objects.filter(catid=catid,title__contains=searchTitle).count() / 2)
    startIndex = 2 * (int(page) - 1)
    endIndex = 2 * int(page)

    #调用方法
    ret=utils.setpage(allPage,page)
    if catid == -1:
        newsList = news.objects.filter(title__contains=searchTitle).order_by('-registtime')[startIndex:endIndex]
    else:
        newsList = news.objects.filter(title__contains=searchTitle,catid=catid).order_by('-registtime')[startIndex:endIndex]
    print("新闻===",newsList)
    # 菜单列表
    menuList = menu.objects.all()
    listinfo = []
    for item in menuList:
        listinfo.append(item)
    # 将页码存进列表中
    allPageList = range(ret[0],ret[1])
    positionName = position.objects.all()
    context = {
        "listinfo": listinfo,
        "newsList":newsList,
        "currentAdmin": currentAdmin,
        "allPageList": allPageList,
        "page": page,
        "catid": catid,
        "searchTitle":searchTitle,
        "menuList":menuList,
        "positionName":positionName,
        "allPage": allPage
    }
    return HttpResponse(template.render(context, request))

# 删除文章列表
def delnews(request):
    # 点击删除按钮  获取id
    newsid = request.GET.get('newsid')
    print(newsid)
    try:
        news.objects.filter(id=newsid).delete()
        return HttpResponse(utils.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(utils.returnResult(1, "删除失败"))

# 添加新闻
def addNews(request):
    template=loader.get_template('admin/news/addNews.html')
    form = TestUEditorForm()
    # 添加颜色列表
    colorList = settings.COLOR_LIST
    # 菜单列表
    menuList = menu.objects.all()
    listinfo = []
    for item in menuList:
        listinfo.append(item)
    context = {
        "listinfo": listinfo,
        "currentAdmin": currentAdmin,
        "form": form,
        "colorList": colorList
    }
    return HttpResponse(template.render(context,request))

# 添加新闻处理
def addNewsHandler(request):
    # 获取前端传递过来的数据存储到数据库
    newsImg = request.FILES.get("newsImg")
    title = request.POST.get('title')
    titlecolor = request.POST.get('titlecolor')
    catid = request.POST.get('catid')
    content = request.POST.get('content')
    print(newsImg,"图片",title,"标题",titlecolor,"颜色",catid,"菜单")
    print(content,"内容")
    now = datetime.now()
    # 按照文章标题判断
    newslist = news.objects.filter(title=title).all()
    if newslist:
        # 不为空时提示该标题已存在
        return HttpResponse(utils.returnResult(1, "该标题已存在，请重新编辑"))
    # 为空时判断缩略图是否为空
    if newsImg:
        # 不为空的时候
        imgSize = utils.getsize(newsImg.size, settings.UPLOADS["unit"])
        if newsImg.name.split(".")[len(newsImg.name.split(".")) - 1] not in settings.UPLOADS["types"]:
            return HttpResponse(utils.returnResult(1, "文件类型不正确"))
        if float(imgSize) > settings.UPLOADS["maxsize"]:
            return HttpResponse(utils.returnResult(1, "文件过大"))
        filename = "newsImg" + str(int(datetime.now().timestamp() * 1000000)) + "." + newsImg.name.split("/")[-1]
        # 对文件是否存在进行判断
        dir = "static/uploads"
        utils.confirmImgFile(dir)
        imgpath = dir + "/" + filename
        with open(imgpath, 'wb') as f:
            for file in newsImg.chunks():
                f.write(file)
                f.flush()
        newarticle = news.objects.create(catid=catid, title=title, title_font_color=titlecolor, thumb=filename, num=0,
                                         registtime=now)
        newid = newarticle.id
        news_content(newsid=newid, content=content).save()
        return HttpResponse(utils.returnResult(0, "添加文章成功"))
    newarticle = news.objects.create(catid=catid, title=title, title_font_color=titlecolor, num=0, registtime=now)
    newid = newarticle.id
    news_content(newsid=newid, content=content).save()
    return HttpResponse(utils.returnResult(0, "添加文章成功"))

# 编辑文章
def editNews(request):
    template = loader.get_template('admin/news/editNews.html')
    form = TestUEditorForm()
    # 添加颜色列表
    colorList = settings.COLOR_LIST
    # 菜单列表
    menuList = menu.objects.all()
    listinfo = []
    for item in menuList:
        listinfo.append(item)
    id = request.GET.get('id')
    print("编辑", id)
    newsInfo = news.objects.filter(id=id)
    newsContent=news_content.objects.values("id","content").filter(newsid=id)
    print(newsContent[0]["content"])
    print(newsInfo[0])
    context = {
        "currentAdmin": currentAdmin,
        "form":form,
        "colorList":colorList,
        "listinfo": listinfo,
        "newsInfo": newsInfo[0],
        "newsContent":newsContent[0]["content"]
    }
    return HttpResponse(template.render(context, request))

# 编辑文章处理
def editNewsHandler(request):
    # 获取前端传递过来的数据存储到数据库
    id = request.POST.get('newsid')
    newsImg = request.FILES.get("newsImg")
    title = request.POST.get('title')
    titlecolor = request.POST.get('titlecolor')
    catid = request.POST.get('catid')
    content = request.POST.get('content')
    print(newsImg, "图片", title, "标题", titlecolor, "颜色", catid, "菜单")
    print(content, "内容")
    print(id)
    now = datetime.now()
    # 为空时判断缩略图是否为空
    if newsImg:
        # 不为空的时候
        imgSize = utils.getsize(newsImg.size, settings.UPLOADS["unit"])
        if newsImg.name.split(".")[len(newsImg.name.split(".")) - 1] not in settings.UPLOADS["types"]:
            return HttpResponse(utils.returnResult(1, "文件类型不正确"))
        if float(imgSize) > settings.UPLOADS["maxsize"]:
            return HttpResponse(utils.returnResult(1, "文件过大"))
        filename = "newsImg" + str(int(datetime.now().timestamp() * 1000000)) + "." + newsImg.name.split("/")[-1]
        # 对文件是否存在进行判断
        dir = "static/uploads"
        utils.confirmImgFile(dir)
        imgpath = dir + "/" + filename
        with open(imgpath, 'wb') as f:
            for file in newsImg.chunks():
                f.write(file)
                f.flush()
                # 删除原来图片
        # newsImg = request.POST.get("newsImg")
        # print("删除", newsImg)
        # path1 = 'static/uploads' + newsImg
        # print(path1,"1234567890-")
        # path=os.path.join(settings.BASE_DIR,path1)
        #
        # os.remove(path)
        #   更新数据库
        newarticle = news.objects.filter(id=id).update(catid=catid, title=title, title_font_color=titlecolor, thumb=filename,
                                         registtime=now)
        news_content.objects.filter(newsid=id).update(content=content)
        return HttpResponse(utils.returnResult(0, "文章修改成功"))
    newarticle = news.objects.filter(id=id).update(catid=catid, title=title, title_font_color=titlecolor,registtime=now)

    news_content.objects.filter(newsid=id).update(content=content)
    return HttpResponse(utils.returnResult(0, "文章修改成功"))

# 添加推荐位内容
def addPosContent(request):
    # 前端传递多个字段的值   用getlist接受
    newsIdList=request.POST.getlist("news")
    positionId = request.POST.get("positionid")
    print(newsIdList,positionId)
    for item in newsIdList:
    #     写入数据库
        position_content.objects.create(newsid=item,positionid=positionId)
    return HttpResponse(utils.returnResult(0, "推荐成功"))

# 推荐位管理
def positionList(request):
    template = loader.get_template('admin/position/position.html')
    positioninfo=position.objects.all()
    print(positioninfo)
    context = {
        "currentAdmin": currentAdmin,
        "positioninfo": positioninfo
    }
    return HttpResponse(template.render(context, request))

# 添加推荐位
def addPosition(request):
    template = loader.get_template('admin/position/addPosition.html')
    context = {
        "currentAdmin": currentAdmin,
    }
    return HttpResponse(template.render(context, request))

# 添加推荐位处理
def addPositionHandler(request):
    positionName = request.POST.get('positionName')
    description= request.POST.get('description')
    status = request.POST.get('status')
    print(status)
    now=datetime.now()
    # 获取符合条件的第一个值
    positionTable = position.objects.filter(name=positionName)
    print(positionTable,"123456789")
    if positionTable:
        print(status)
        return HttpResponse(utils.returnResult(1, "该推荐位已存在，请重新编辑", status))
    addPositionTable = position(name=positionName,description=description,createTime=now).save()
    return HttpResponse(utils.returnResult(0, "推荐位增加成功", status))

# 编辑推荐位
def editPosition(request):
    template = loader.get_template('admin/position/editPosition.html')
    id=request.GET.get("posId")
    print(id)
    positionList=position.objects.filter(id=id)
    print(positionList[0])
    context = {
        "currentAdmin": currentAdmin,
        "positionList":positionList[0]
    }
    return HttpResponse(template.render(context, request))


# 编辑推荐位处理
def editPositionHandler(request):
    id=request.POST.get('id')
    positionName = request.POST.get('positionName')
    description= request.POST.get('description')
    status = request.POST.get('status')
    print(status)
    now=datetime.now()
    addPositionTable = position.objects.filter(id=id).update(name=positionName,description=description,createTime=now)
    return HttpResponse(utils.returnResult(0, "推荐位修改成功", status))

# 删除推荐位
def delPosition(request):
    # 点击删除按钮  获取id
    posid = request.GET.get('posid')
    print(posid)
    try:
        position.objects.filter(id=posid).delete()
        return HttpResponse(utils.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(utils.returnResult(1, "删除失败"))

# 推荐位内容管理
def poscontent(request):
    template = loader.get_template('admin/position/positionContent.html')
    # option 搜索  获取id
    posid = -1
    if request.GET.get("id"):
        posid = int(request.GET.get("id"))
    print("我是id", posid)
    # 分页   首先判断当前有没有页数  设定默认值为第一页
    page = 1
    if request.GET.get("page"):
        page = int(request.GET.get("page"))
    print(request.GET.get("page"))
    # 当前总页数向上取整
    if posid == -1:
        allPage = math.ceil(position_content.objects.all().count() / 2)
    else:
        allPage = math.ceil(position_content.objects.filter(positionid=posid).count() / 2)
    startIndex = 2 * (int(page) - 1)
    endIndex = 2 * int(page)
    # 调用分页方法
    ret=utils.setpage(allPage,page)
    if posid == -1:
        posConList = position_content.objects.all().order_by("-id")[startIndex:endIndex]
    else:
        posConList = position_content.objects.filter(positionid=posid).order_by("-id")[startIndex:endIndex]
    # 分页索引值存入列表
    allPageList = range(ret[0],ret[1])
    # 遍历positionContent  存入列表
    infoList=[]
    for item in posConList:
        infoObj = {}
        # 推荐为内容id
        infoObj["id"]=item.id
        newsList=news.objects.values("title","thumb").filter(id=item.newsid)
        for i in newsList:
            infoObj["title"]=i["title"]
            infoObj["thumb"] = i["thumb"]
        positionList=position.objects.values("name").filter(id=item.positionid)
        for p in positionList:
            infoObj["posName"] = p["name"]
        infoList.append(infoObj)
    # 获取推荐位列表
    positioninfo = position.objects.all()
    context = {
        "currentAdmin": currentAdmin,
        "positioninfo":positioninfo,
        "infoList":infoList,
        "allPageList": allPageList,
        "page": page,
        "posid":posid,
        "allPage": allPage
    }
    return HttpResponse(template.render(context, request))

# 删除推荐位内容
def delPoscontent(request):
    # 点击删除按钮  获取id
    posid = request.GET.get('posid')
    print(posid)
    try:
        position_content.objects.filter(id=posid).delete()
        return HttpResponse(utils.returnResult(0, "删除成功"))
    except Exception as e:
        return HttpResponse(utils.returnResult(1, "删除失败"))

# 编辑推荐位内容
def editposContent(request):
    template = loader.get_template('admin/position/editposContent.html')
    # 获取推荐位内容id
    id = request.GET.get("id")
    print(id)
    posConList=position_content.objects.values("newsid","positionid").filter(id=id)
    infoList = []
    newsInfo=news.objects.values("title","thumb").filter(id=posConList[0]["newsid"])
    positionInfo=position.objects.values("id","name").filter(id=posConList[0]["positionid"])
    print("新闻",newsInfo[0])
    print("推荐位",positionInfo[0])
    positionList = position.objects.all()
    context = {
        "currentAdmin": currentAdmin,
        "positionList":positionList,
        "newsInfo": newsInfo[0],
        "positionInfo":positionInfo[0],
        "id":id
    }
    return HttpResponse(template.render(context, request))

# 编辑推荐位内容处理
def editposContentHandler(request):
    id = request.POST.get("posContentId")
    posid = request.POST.get('posid')
    title = request.POST.get('title')
    status = request.POST.get('status')
    newsid=news.objects.filter(title=title).values("id")
    position_content.objects.filter(id=id).update(newsid=newsid[0]["id"],positionid=posid)
    return HttpResponse(utils.returnResult(0, "推荐位内容修改成功", status))

# 删除多余文件
def clearFile(request):
    # 首先获取数据库中的文件
    excessFile=news_content.objects.values("content")
    imgList=[]
    pattern = '<img src="/static/uploads/(.*?)".*?/>'
    for item in excessFile:
        print("1234567890-=",item["content"])
        result = re.findall(pattern, item["content"])
        print(result)
        if result:
            imgList.extend(result)
    print("我是图片",imgList)

    # 获取本地文件夹中的图片
    path = os.path.join(os.getcwd(), "static/images/")
    # 调用方法
    filesList=utils.getFilesName(path)
    print(filesList,"文件数量")
    for file in filesList:
        imgpath = os.path.join(path, file)
        if file in imgList:
            #表示存在
            pass
        else:
            os.remove(file)
    return HttpResponse('<script>alert("清理成功")</script>')
