from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response,send_from_directory  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
import datetime
import xlrd
import math
ribao=Blueprint("ribao",__name__)
@ribao.route("/selectclass")
def selectclass():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from classes")
    result=cursor.fetchall()
    return json.dumps(result,default=str)
@ribao.route("/selectcourse")
def selectcourse():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from course")
    result=cursor.fetchall()
    return json.dumps(result,default=str)
@ribao.route("/select")
def select():
    course=request.args.get("course")
    classes=request.args.get("classes")
    # params = ""
    # if (course == "0"):           #关联查询
    #     if(classes=="0"):
    #         params="select logs.*,student.sname as sname,classes.name as cname from logs left join student on logs.phone=student.phone left join classes on student.classid=classes.id"
    #     else:
    #         params="select logs.*,student.sname,classes.name as cname from logs,student,classes where student.phone=logs.phone and student.classid=classes.id and classes.id=%s"%(classes)
    # else:
    #     if(classes == "0"):
    #         params = "select logs.*,student.sname,classes.name as cname from logs,student,classes where student.phone=logs.phone and student.classid=classes.id and classes.cid=%s"%(course)
    #     else:
    #         params="select logs.*,student.sname,classes.name as cname from logs,student,classes where student.phone=logs.phone and student.classid=%s and student.classid=classes.id and classes.cid=%s"%(classes,course)
    # db = pymysql.connect(host='localhost',
    #                      user='root',
    #                      password='03145658159shen',
    #                      db='youyike',
    #                      charset='utf8mb4',
    #                      cursorclass=pymysql.cursors.DictCursor)
    # cursor = db.cursor()
    # cursor.execute(params)
    # result = cursor.fetchall()
    # cursor.close()
    # db.close()
    # limit=pages(len(result),2)["limit"]
    # print(limit)
    # db = pymysql.connect(host='localhost',
    #                      user='root',
    #                      password='03145658159shen',
    #                      db='youyike',
    #                      charset='utf8mb4',
    #                      cursorclass=pymysql.cursors.DictCursor)
    # cursor = db.cursor()
    # cursor.execute(params+" "+limit)
    # result1 = cursor.fetchall()
    # pagestr=pages(len(result),2)["pagestr"]
    # if(result1):
    #     result1[0]["pagestr"]=pagestr
    # return json.dumps(result1, default=str)
    params = ""
    if (course == "0"):                     #子查询
        if (classes == "0"):
            params = "select logs.*,student.sname as sname,classes.name as cname from logs left join student on logs.phone=student.phone left join classes on student.classid=classes.id where 1=1"
        else:
            params="select logs.*,student.sname as sname,classes.name as cname from logs left join student on logs.phone=student.phone left join classes on student.classid=classes.id where logs.phone in (select phone from student where classid in (%s))"% (classes)
    else:
        if(classes == "0"):
            params = "select logs.*,student.sname as sname,classes.name as cname from logs left join student on logs.phone=student.phone left join classes on student.classid=classes.id where logs.phone in (select phone from student where classid in (select id from classes where cid =%s))" %(course)
        else:
            params = "select logs.*,student.sname as sname,classes.name as cname from logs left join student on logs.phone=student.phone left join classes on student.classid=classes.id where logs.phone in (select phone from student where classid in (select id from classes where cid=%s and id=%s))" %(course, classes)
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute(params)
    result = cursor.fetchall()
    # limit = pages(len(result), 2)["limit"]
    return json.dumps(result,default=str)
# select logs.*,stu.name as sname,classes.name as cname from logs left join stu on logs.phone=stu.phone left join classes on stu.classid=classes.id where logs.phone in (select phone from stu where classid in (select id from classes where fid in (10)) and date.format(logs.time,"%Y-%m-%d")="2018-11-11") limit  0,5
def pages(total,pageNum):               #参数一共多少跳数据，每页几条数据
    if request.url.find("?")<0:         #判断请求是否有？号，没有在末尾加上?page=
        url=request.url+"?page="
    else:
        if request.url.rfind("page")<0:  #判断请求是否含有page，没有加上&page=
            url=request.url+"&page="
        else:
            url=request.url[0:request.url.rfind("=")+1]  #有，去掉page原有的值
    currentpage=int(request.args.get("page") or 0)     #从请求中获取到当前页
    pageNums=math.ceil(total/pageNum)                #向上取整，得到页数
    pagestr=""
    pagestr+="共%s页"%(pageNums)
    pagestr+="<a href='%s'>首页</a>"%(url+"0")
    last=currentpage-1 if currentpage-1>0 else 0
    pagestr+="<a href='%s'>上一页</a>" %(url+str(last))
    start=currentpage-2 if currentpage-2>0 else 0
    end=currentpage+2 if currentpage+2>pageNums else pageNums
    for item in range(start,end):
        if(currentpage==item):
            pagestr+="<a href='%s' style='color:red'>[%s]</a>"%(url+str(item),item+1)
        else:
            pagestr += "<a href='%s'>[%s]</a>" % (url + str(item), item + 1)
    next=currentpage+1 if currentpage+1<pageNums else pageNums-1
    pagestr+="<a href='%s'>下一页</a>" %(url+str(next))
    pagestr += "<a href='%s'>尾页</a>" % (url + str(pageNums-1))
    limit="limit"+" "+str(currentpage)+","+str(pageNum)
    jieguo={"pagestr":pagestr,"limit":limit}
    return jieguo

@ribao.route("/xiangqing")
def xiangqing():
    id=request.args.get("id")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from logs where id=%s",(id))
    result=cursor.fetchone()
    return json.dumps(result,default=str)
@ribao.route("/submitribao")
def submitribao():
    phone=request.args.get("phone")
    title=request.args.get("title")
    con=request.args.get("con")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into logs (phone,title,con) values (%s,%s,%s)",(phone,title,con) )
    db.commit()
    return "ok"
@ribao.route("/teacherselect")
def teacherselect():
    phone=request.args.get("phone")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select logs.*,student.sname,classes.name as cname from logs,student,classes,teacher where logs.phone=student.phone and student.classid=teacher.clid and teacher.clid=classes.id and teacher.phone=%s",(phone))
    result=cursor.fetchall()
    return json.dumps(result,default=str)
@ribao.route("/studentselect")
def studentselect():
    phone=request.args.get("phone")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select logs.*,student.sname,classes.name as cname from logs,student,classes where logs.phone=student.phone and student.classid=classes.id and student.phone=%s",(phone))
    result = cursor.fetchall()
    return json.dumps(result, default=str)