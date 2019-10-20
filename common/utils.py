import json
import math
import os
# 公共返回数据
def returnResult(code,mgs,data="",data1="",data2=""):
    '''
    :param code: 0代表success ！=0 代表error
    :param mgs:  返回的信息
    :param data: 返回扥数据
    :return:
    '''
    returndata1={
        "code":code,
        "mgs":mgs,
        "data":data,
        "data1":data1,
        "data2":data2
    }
    returndata = json.dumps(returndata1)
    return returndata

# 单位转换：
# B转成  kb  mb  gb
def getsize(size, format = 'kb'):
    p = 0
    if format == 'kb':
        p = 1
    elif format == 'mb':
        p = 2
    elif format == 'gb':
        p = 3

    size /= math.pow(1024, p)

    return "%0.2f"%size;


# 存储缩略图文件是否存在进行确认
def confirmImgFile(dir):
#     首先对参数进行截取   eg：/static/uploads...
    dirList=dir.split("/")
    for k,v in enumerate(dirList):
#         拼接绝对路径
        currentdir=os.path.join(os.getcwd(),v)
        # 判断当前文件夹是否存在
        if not os.path.exists(currentdir):
            os.mkdir(currentdir)
        # 取上一索引值与之进行拼接
        if k<len(dirList)-1:
            dirList[k+1]=os.path.join(v,dirList[k+1])

# 分页方法
def setpage(allPage,currentPage):     #参数为  总页数   当前页码
    # 一次显示3页  0-3 3-6  6-9
    pageNum=3  #一次显示3页
    startPage=1
    endPage=3
    print("总页数",allPage,"当前",currentPage)
    if (currentPage <= pageNum / 2):
        startPage = 1
        endPage = pageNum
    # 判断总条数<= 3 每页显示3条数据
    else:
        startPage = math.ceil(currentPage - pageNum / 2)
        endPage = math.ceil(currentPage + pageNum / 2 - 1)
        print("当前页码22", currentPage, "开始值", startPage, "结束值", endPage)
    # 判断如果开始值小于1

    # 判断如果结束值>总页数   给结束值赋值为总页数
    if endPage>=allPage:
        endPage=allPage
        startPage=endPage-pageNum+1
        print("当前页码44", currentPage, "开始值", startPage, "结束值", endPage)
    if startPage < 1:
        startPage = 1
        endPage = pageNum
        print("当前页码33", currentPage, "开始值", startPage, "结束值", endPage)
    return startPage, endPage+1




# 分页算法
def getViewPage(allPage, currentPage):
    '''
    :param allPage:      总页码
    :param currentPage:  当前的页码
    每一屏幕显示几个页码
    startPindex  endPIndex
    :return:
    '''

    # 三种  1，2，3             8，9，10
    #
    pageNow = currentPage  # 当前页码
    pageNum = 3  # 要显示的页数
    pageStart = 1  # 开始页码
    pageEnd = 3  # 结束页码
    pageCount = allPage  # 总页数  2

    # allcout=2
    #   1        3/2=1.5
    #   2        3/2=1.5     s=1   e=3
    #   3       3/2=1.5     s=2   e=4
    #   4                   s=3   e=5
    #   5                  s=4   e=6
    if (pageNow <= pageNum / 2):
        pageStart = 1
        pageEnd = pageNum
    else:  # 2   3/2   2-3/2 =1,   3-3/2 =2,   3+1.5-1=4  2+1.5-1=3
        pageStart = math.ceil(pageNow - pageNum / 2)
        pageEnd = math.ceil(pageNow + pageNum / 2 - 1)

    # 对pageEnd 进行校验，并重新赋值
    if (pageEnd > pageCount):  # 3>2
        pageEnd = pageCount  # 2
        pageStart = pageEnd - (pageNum - 1)  # 0
    pageStart = 1 if pageStart < 1 else pageStart

    print("总页数=", pageCount, "--开始页码=", pageStart, "---结束页码=", pageEnd)
    return pageStart,pageEnd+1




# 2.查找文件
filesList=[]
def getFilesName(path):
    global filesList
    # print(path)
    if not os.path.exists(path):
        # print("当前文件/文件夹不存在")
        return
    if os.path.isfile(path):
        # print("文件")
        filesList.append(path)
        return
    dirList=os.listdir(path)
    if dirList==[]:
        # print("文件夹是空的文件夹")
        return
    for item in dirList:
        # 得到item的完整的路径
        itemPath=os.path.join(path,item)
        if os.path.isfile(itemPath):
            # print("item是文件")
            filesList.append(item)
        else:
            # print("item是文件夹")
            getFilesName(itemPath)
    return filesList



# path=os.path.join(os.getcwd(),"test2")
# getFilesName(path)
# print(filesList)


