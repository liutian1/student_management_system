import pymysql

# user = input("user:")
# password = input("password:")

conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="123456",database="db3")
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# sql = "select * from userinfo where user=%s and password=%s"
sql = "insert into userinfo (user,password) values(%s,%s)"


# cursor.execute(sql,[user,password])
cursor.callproc('p3',(1,1))
conn.commit()
# result = cursor.fetchone()
#
# if result:
#     print("ok")
# else:
#     print("error")
result = cursor.fetchall()
print(result)

cursor.execute('select @_p3_0,@_p3_1')
result = cursor.fetchall()
print(result)
cursor.close()
conn.close()