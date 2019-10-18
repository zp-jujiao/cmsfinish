from django.shortcuts import render
from django.template import loader
from django.shortcuts import render, redirect, HttpResponse
from admin1.models import *
from django.conf import settings
import json
import math

# Create your views here.
list=''
newslist1=[]
newslist2=[]
contentlist=[]
positionthreelist=[]
index=''
def home(request):
    template=loader.get_template('index/home.html')
    global list
    list=menu.objects.values("name","id").all()
    left()
    positionone=position_content.objects.filter(positionid=1).all()[0:3]
    positiontwo=position_content.objects.filter(positionid=2).all()[0:3]
    positiononelist=[]
    positiontwolist = []
    for item in positionone:
        positiononeinfo=news.objects.filter(id=item.newsid)
        for item11 in positiononeinfo:
            print(item11.id,item11.thumb,item11.title)
            positiononedict={"id":item11.id,"thumb":item11.thumb,"title":item11.title}
            positiononelist.append(positiononedict)
    print(positiononelist)
    for item1 in positiontwo:
        positiontwoinfo = news.objects.filter(id=item1.newsid)
        for item12 in positiontwoinfo:
            print(item12.id, item12.thumb, item12.title)
            positiontwodict = {"id": item12.id, "thumb": item12.thumb, "title": item12.title}
            positiontwolist.append(positiontwodict)
    context = {"menulist":list,"index":0,"news": newslist2,"positionone":positiononelist,"positiontwo":positiontwolist,"positionthree":positionthreelist}
    return HttpResponse(template.render(context,request))

def detail(request):
    template=loader.get_template('index/detail.html')
    print(list)
    left()
    context = {"menulist":list,"news": newslist2,"positionthree":positionthreelist}
    return HttpResponse(template.render(context,request))

# def subpage(request):
#     template=loader.get_template('index/subpage.html')
#     id = request.GET.get('id')
#     newscount = news.objects.filter(catid=id).all().count()
#     newspage = math.ceil(newscount / 6)
#     list2 = []
#     num = 1
#     for i in range(0, newspage):
#         list2.append(num)
#         num += 1
#     left()
#     print(index)
#     context = {"menulist":list,"index":int(index),"news": newslist2,"list":list2,"positionthree":positionthreelist}
#     print(context)
#     return HttpResponse(template.render(context,request))

def subpage(request):
    id = request.GET.get('id')
    left()
    newscount=news.objects.filter(catid=id).all().count()
    newspage=math.ceil(newscount/6)
    page = 1
    pages=settings.PAGES
    if request.GET.get('page'):
        page=request.GET.get('page')
        print(type(page),"我是page",page)
    firstpagenum = (int(page)-1) * pages
    lastpagenum = int(firstpagenum) + pages
    pagelist = []
    for i in range(0,newspage):
        pagelist.append(i+1)
    newsinfo = news.objects.filter(catid=id).order_by('-registtime').all()[firstpagenum:lastpagenum]
    global contentlist
    global newslist1
    contentlist = []
    newslist1 = []
    for item in newsinfo:
        content = news_content.objects.filter(newsid=item.id).values("content", "id")
        newsdict = {"id": item.id, "title": item.title, "titlecolor": item.title_font_color, "thumb": item.thumb,
                    "num": item.num, "registtime": item.registtime,"content":content[0]["content"] }
        newslist1.append(newsdict)
        for item1 in content:
            contentdict = {"id": item1["id"], "content": item1["content"]}
            print(contentdict)
            contentlist.append(contentdict)

    return render(request, "index/subpage.html", {"content":contentlist, "index":index, "newslist":newslist1,"page":int(page), "pagelist":pagelist,"positionthree":positionthreelist,"menulist":list,"news": newslist2})


def subpage1(request):
    global index
    index = int(request.GET.get('index'))
    data={"index":index}
    index1=json.dumps(data)
    response = HttpResponse(index1)
    response["Access-Control-Allow-Origin"] = "*"
    return response
    # template=loader.get_template('index/subpage.html')
    # newscount = news.objects.filter(catid=2).all().count()
    # newspage = math.ceil(newscount / 6)
    # list2 = []
    # num = 1
    # for i in range(0, newspage):
    #     list2.append(num)
    #     num += 1
    # left()
    # context = {"menulist":list,"index":2,"news": newslist2,"list":list2}
    # return HttpResponse(template.render(context,request))

def subpage2(request):
    template=loader.get_template('index/subpage.html')
    newscount = news.objects.filter(catid=3).all().count()
    newspage = math.ceil(newscount / 6)
    list2 = []
    num = 1
    for i in range(0, newspage):
        list2.append(num)
        num += 1
    left()
    context = {"menulist":list,"index":3,"news": newslist2,"list":list2}
    return HttpResponse(template.render(context,request))

def subajax(request):
    menuid = request.GET.get('id')
    pagenum=request.GET.get('num')
    firstpagenum=int(pagenum)*6
    lastpagenum=int(firstpagenum)+6
    newslist=news.objects.filter(catid=menuid).order_by('-registtime').all()[firstpagenum:lastpagenum]
    newscount=news.objects.filter(catid=menuid).all().count()
    newspage=math.ceil(newscount/6)
    num=1
    list=[]
    for i in range(0,newspage):
        list.append(num)
        num+=1
    print(list)
    global contentlist
    global newslist1
    contentlist=[]
    newslist1=[]
    for item in newslist:
        newsdict={"id":item.id,"title":item.title,"titlecolor":item.title_font_color,"thumb":item.thumb,"num":item.num,"registtime":datetime.timestamp(item.registtime)}
        newslist1.append(newsdict)
        print(newslist1)
        content=news_content.objects.filter(newsid=item.id).values("content","id")
        print(content)
        for item1 in content:
            contentdict={"id":item1["id"],"content":item1["content"]}
            print(contentdict)
            contentlist.append(contentdict)
    print(contentlist)
    dic={
        "news":newslist1,
        "cont":contentlist,
        "list":list,
    }
    userinfodata = json.dumps(dic)
    response = HttpResponse(userinfodata)
    response["Access-Control-Allow-Origin"] = "*"
    return response


def detailajax(request):
    newsid = request.GET.get('newsid')
    print(newsid)
    numdata=news.objects.filter(id=newsid).values("num")
    newsnum=int(numdata[0]["num"])+1
    print(newsnum)
    news.objects.filter(id=newsid).update(num=newsnum)
    detailnews = news.objects.filter(id=newsid)
    newsinfo = {}
    for item in detailnews:
        newsdict={"id":item.id,"title":item.title,"titlecolor":item.title_font_color,"thumb":item.thumb,"num":item.num,"registtime":datetime.timestamp(item.registtime)}
        print(newsdict,"我是news")
        newsinfo["news"] = newsdict
    detailcont = news_content.objects.filter(newsid=newsid)
    for item1 in detailcont:
        contdict={"content":item1.content}
        print(contdict,"我是cont")
        newsinfo["cont"]=contdict
    # newsinfo={
    #     "news":newsdict,
    #     "cont":contdict,
    # }
    newsinfodata = json.dumps(newsinfo)
    response = HttpResponse(newsinfodata)
    response["Access-Control-Allow-Origin"] = "*"
    return response



def homeajax(request):
    menuid = request.GET.get('id')
    newslist=news.objects.order_by('-registtime').all()[0:4]
    global contentlist
    global newslist1
    contentlist=[]
    newslist1=[]
    for item in newslist:
        newsdict={"id":item.id,"title":item.title,"titlecolor":item.title_font_color,"thumb":item.thumb,"num":item.num,"registtime":datetime.timestamp(item.registtime)}
        newslist1.append(newsdict)
        print(newslist1)
        content=news_content.objects.filter(newsid=item.id).values("content","id")
        print(content)
        for item1 in content:
            contentdict={"id":item1["id"],"content":item1["content"]}
            print(contentdict)
            contentlist.append(contentdict)
    print(contentlist)
    dic={
        "news":newslist1,
        "cont":contentlist,
    }
    userinfodata = json.dumps(dic)
    response = HttpResponse(userinfodata)
    response["Access-Control-Allow-Origin"] = "*"
    return response


def left():
    newsranklist = news.objects.order_by('-num').all()[0:5]
    positionthree=position_content.objects.filter(positionid=3).all()[0:3]
    global newslist2
    global positionthreelist
    newslist2 = []
    positionthreelist=[]
    num=1
    for item in newsranklist:
        if num<6:
            newsdict={"id":item.id,"title":item.title,"titlecolor":item.title_font_color,"thumb":item.thumb,"num":item.num,"registtime":datetime.timestamp(item.registtime),"index":num}
            newslist2.append(newsdict)
            num+=1
    for item1 in positionthree:
        positionthreeinfo=news.objects.filter(id=item1.newsid)
        for item22 in positionthreeinfo:
            positionthreedict={"id": item22.id, "thumb": item22.thumb, "title": item22.title}
            positionthreelist.append(positionthreedict)