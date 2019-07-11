from django.shortcuts import render,redirect,HttpResponse
import pymysql
from utils import sqlheper
import json

def classes(request):
    conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="123456",db="oldboy",charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,name from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,"classes.html",{"class_list":class_list})


def add_class(request):

    if request.method == "GET":
        return render(request,"add_class.html")
    else:
        print(request.POST)
        v = request.POST.get("name")
        if len(v) > 0:
            conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="oldboy", charset="utf8")
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            cursor.execute("insert into class(name) values (%s)",[v,])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect("/classes")
        else:
            return render(request,"add_class.html",{"msg":"班级名称不能为空"})

def del_class(request):
    nid = request.GET.get("nid")
    conn = pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="123456",db="oldboy", charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where id=%s",[nid,])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/classes/")

def edit_class(request):

    if request.method == "GET":
        nid = request.GET.get('nid')
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="oldboy", charset="utf8")

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,name from class where id = %s", [nid, ])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(result)
        return render(request, 'edit_class.html', {'result': result})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="oldboy", charset="utf8")

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set name=%s where id = %s", [name, nid, ])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/classes/')

def students(request):
    """
    学生表
    :param request:
    :return:
    """
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="oldboy", charset="utf8")

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select student.id,student.sname,student.class_id,class.name from student left join class on student.class_id = class.id;"
    cursor.execute(sql)
    student_list = cursor.fetchall()
    cursor.close()
    conn.close()
    class_list = sqlheper.get_list("select id ,name from class;",[])

    return render(request,"students.html",{"student_list":student_list,"class_list":class_list})

def add_student(request):
    if request.method == "GET":
        conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="123456",db="oldboy",charset="utf8")
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,name from class")
        class_list = cursor.fetchall()
        cursor.close()
        conn.close()

        return render(request,"add_student.html",{"class_list":class_list})
    else:
        name = request.POST.get("name")
        class_id = request.POST.get("class_id")
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='oldboy', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into student(sname,class_id) values(%s,%s)", [name, class_id, ])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/students/")

def del_student(request):
    nid = request.GET.get("nid")
    conn = pymysql.connect(host="127.0.0.1", port=3306,user="root",passwd="123456",db="oldboy", charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from student where id=%s",[nid,])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/students/")

def edit_student(request):
    if request.method == "GET":
        nid = request.GET.get("nid")
        class_list = sqlheper.get_list("select id,name from class",[])
        current_student_info = sqlheper.get_one('select id,sname,class_id from student where id=%s', [nid, ])
        return render(request, 'edit_student.html',
                      {'class_list': class_list, 'current_student_info': current_student_info})
    else:
        nid = request.GET.get("nid")
        name = request.POST.get('sname')
        class_id = request.POST.get('class_id')
        sqlheper.modify('update student set sname=%s,class_id=%s where id=%s', [name, class_id, nid, ])
        return redirect('/students/')

def modal_add_class(request):
    name = request.POST.get("name")
    if len(name)>0:
        sqlheper.modify("insert into class(name) values (%s)",[name,])
        return HttpResponse("ok")
    else:
        return HttpResponse('班级标题不能为空')


def modal_edit_class(request):
    name = request.POST.get("name")
    nid = request.POST.get("nid")
    if len(name) > 0:
        sqlheper.modify("update class set name=%s where id=%s", [name, nid,])
        return HttpResponse("ok")
    else:
        return HttpResponse('班级不能为空')

def model_add_student(request):
    ret = {"status":True,"message":None}
    try:
        name = request.POST.get("sname")
        class_id = request.POST.get("class_id")
        sqlheper.modify("insert into student(sname,class_id) values (%s,%s)",[name,class_id,])
    except Exception as e:
        ret["status"] = False
        ret["message"] = str(e)
    return HttpResponse(json.dumps(ret))


def modal_edit_student(request):
    ret = {"status":True,"message":None}
    try:
        sname = request.POST.get("name")
        nid =  request.POST.get("nid")
        class_id = request.POST.get("class_id")
        sqlheper.modify("update student set sname=%s,class_id=%s where id=%s",[sname,class_id,nid,])
    except Exception as e:
        ret["status"] = False
        ret["message"] = str(e)
    return HttpResponse(json.dumps(ret))

def teachers(request):

    teacher_list = sqlheper.get_list("select teacher.id as tid,teacher.name,class.name as cname from teacher left join teacher2class on teacher.id=teacher2class.teacher_id left join class on class.id = teacher2class.class_id;",[])
    result = {}
    # print(teacher_list)
    for row in teacher_list:
        tid = row["tid"]
        if tid in result:
            result[tid]["cnames"].append(row["cname"])
        else:
            result[tid] = {"tid":row["tid"],"name":row["name"],"cnames":[row["cname"],]}

    return render(request,"teachers.html",{"teacher_list":result.values()})


def add_teacher(request):
    if request.method == "GET":
        class_list = sqlheper.get_list('select id,name from class', [])
        return render(request, 'add_teacher.html', {'class_list': class_list})

    else:
        name = request.POST.get('name')
        teacher_id = sqlheper.create('insert into teacher(name) values(%s)', [name, ])
        class_ids = request.POST.getlist('class_ids')
        print(class_ids)
        data_list = []
        for cls_id in class_ids:
            temp = (teacher_id,cls_id)
            data_list.append(temp)
        obj = sqlheper.SqlHelper()
        obj.multiple_modify("insert into teacher2class (teacher_id,class_id) values (%s,%s)",data_list)
        obj.close()
        return redirect("/teachers/")


def edit_teacher(request):
    pass

def get_all_class(request):
    obj = sqlheper.SqlHelper()
    class_list = obj.get_list('select id,name from class', [])
    obj.close()
    return HttpResponse(json.dumps(class_list))
def test(request):
    return render(request, "test.html")

def layout(request):
    return render(request,"layout.html")

