from flask import Flask,render_template,redirect,request,session,make_response  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
from publick.image import code
from publick.menus import menu
app=Flask(__name__)
from url.user import user
from url.role import role
from url.course import course
from url.classes import classes
from url.student import student
from url.teacher import teacher
from url.ribao import ribao
from url.shiti import shiti
from url.shijuan import shijuan
from url.test import test
# response.setHeader("Access-Control-Allow-Credentials","true");
app.register_blueprint(user,url_prefix="/ajax/user/")
app.register_blueprint(role,url_prefix="/ajax/role/")
app.register_blueprint(course,url_prefix="/ajax/course/")
app.register_blueprint(classes,url_prefix="/ajax/classes/")
app.register_blueprint(student,url_prefix="/ajax/student/")
app.register_blueprint(teacher,url_prefix="/ajax/teacher/")
app.register_blueprint(ribao,url_prefix="/ajax/ribao/")
app.register_blueprint(shiti,url_prefix="/ajax/shiti/")
app.register_blueprint(shijuan,url_prefix="/ajax/shijuan/")
app.register_blueprint(test,url_prefix="/ajax/test/")
app.secret_key=("123456")
# rid1=0
# id1=0
@app.before_request   #在每次请求之前执行
def before_request():
    if request.path!="/logins" and request.path!="/getma":   #请求的路径不等于logins
        if (session.get("rid")):
            if request.path!="/":
                return redirect("/")
#登陆页面
@app.route("/")
def login():
    aa = session.get("login")  # session的获取
    if (aa=="yes"):
        return redirect("http://localhost:8080")
    else:
        return render_template("login.html")
#注册页面
@app.route("/zhuce")
def zhuce():
    return render_template("zhuce.html")
#帐号密码的检验
@app.route("/logins",methods=["POST"])
def logins():
    phone=request.form["phone"]
    password=request.form["password"]
    yanma=request.form["yanma"]
    yanma=yanma.lower()
    md5=hashlib.md5()
    md5.update(password.encode("utf-8"))
    password=md5.hexdigest()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from user where phone=%s and password=%s",(phone,password))
    result=cursor.fetchone()
    if(result and yanma==session.get("yanma")):
        rid = result["rid"]
        id = result["id"]
        res = make_response(redirect("/"))
        res.headers["Access-Control-Allow-Credentials"]=True
        # res.set_cookie("login","yes")
        session["login"]="yes"
        session["rid"] = rid
        session["id"]=id
        global rid1
        global id1
        rid1=session.get("rid")
        id1=session.get("id")
        return res
        # return "ok"
    else:
        return redirect("/")
# 权限查询
# @app.route("/ajax/selectpower")
# def selectpower():
#     global arr
#     arr=[]
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='03145658159shen',
#                          db='youyike',
#                          charset='utf8mb4',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = db.cursor()
#     cursor.execute("select * from power where name=%s",(rid1))
#     result=cursor.fetchall()
#     results = digui(result, 0)
#     return json.dumps(results)
# arr = []
# def digui(data, pid, now=None):
#     global arr
#     for item in data:
#         if item["pid"] == pid:
#             if not "children" in item:
#                 item["children"] = []
#             if item["pid"] == 0:
#                 item["con"] = item["con"]
#                 item["name"] = item["name"]
#                 arr.append(item)
#             else:
#                 item["con"] = item["con"]
#                 item["name"] = item["name"]
#                 now.append(item)
#             digui(data, item["id"], item["children"])
#     return arr
#查看menu中的数据
@app.route("/ajax/selectmenu")
def selectmenu():
    return json.dumps(menu)
@app.route("/ajax/selectpower")
def selectpower():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from user,role where user.rid=role.id and user.id=%s",(id1))
    result=cursor.fetchone()
    return json.dumps(result)
@app.route("/exit")
def exit():
    return redirect("/")
#验证码的使用
@app.route("/getma")
def getma():
    codeobj = code()
    codeobj.lineNum = 5
    res = make_response(codeobj.output())
    session["yanma"]=codeobj.str
    res.headers['content-type'] = "image/png"
    return res
#用户的注册添加
# @app.route("/ajax/adduser",methods=["POST"])
# def adduser():
#     name=request.form["name"]
#     password=request.form["password"]
#     phone = request.form["phone"]
#     profession = request.form["profession"]
#     md5 = hashlib.md5()
#     md5.update(password.encode("utf-8"))
#     password = md5.hexdigest()
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='03145658159shen',
#                          db='youyike',
#                          charset='utf8mb4',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = db.cursor()
#     cursor.execute("insert into user (name,password,phone,rid) values (%s,%s,%s,%s)",(name,password,phone,profession))
#     db.commit()
#     return render_template("tishi.html")
# def adduser():
#     name=request.form['name']
#     password=request.form['password']
#     phone=request.form['phone']
#     rid=request.form['inlineRadioOptions']
#     db = pymysql.connect(host='localhost',
#                                   user='root',
#                                   password='03145658159shen',
#                                   db='youyike',
#                                   charset='utf8mb4',
#                                   cursorclass=pymysql.cursors.DictCursor)
#     cursor = db.cursor()
#     cursor.execute("insert into user (name,password,phone,rid) values (%s,%s,%s,%s)",(name,password,phone,rid))
#     db.commit()
#     return redirect("http://localhost:8080/#/selectuser")
#删除用户
# @app.route("/ajax/delete")
# def delete():
#     id=request.args.get("id")
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='03145658159shen',
#                          db='youyike',
#                          charset='utf8mb4',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = db.cursor()
#     cursor.execute("delete from user where id=%s",(id))
#     db.commit()
#     return "ok"
#查找修改用户
# @app.route("/ajax/selectchange")
# def selectchange():
#     id=request.args.get("id")
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='03145658159shen',
#                          db='youyike',
#                          charset='utf8mb4',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = db.cursor()
#     cursor.execute("select * from user where id=%s",(id))
#     result=cursor.fetchone()
#     return json.dumps(result)
#修改用户信息
# @app.route("/ajax/changeuser",methods=["POST"])
# def changeuser():
#     id=request.form["id"]
#     name = request.form["name"]
#     phone= request.form["phone"]
#     rid = request.form["inlineRadioOptions"]
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='03145658159shen',
#                          db='youyike',
#                          charset='utf8mb4',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = db.cursor()
#     cursor.execute("update user set name=%s,phone=%s,rid=%s where id=%s",(name,phone,rid,id))
#     db.commit()
#     return redirect("http://localhost:8080/#/selectuser")
# #查看用户
# @app.route("/ajax/selectuser")
# def selectuser():
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='03145658159shen',
#                          db='youyike',
#                          charset='utf8mb4',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = db.cursor()
#     cursor.execute("select * from user")
#     result=cursor.fetchall()
#     return json.dumps(result)





















app.run()