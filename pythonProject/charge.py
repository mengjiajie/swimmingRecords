import mysql.connector

# 连接到数据库
config = {
    'user': 'yourusername',
    'password': 'yourpassword',
    'host': 'localhost',
    'database': 'yourdatabase'
}
cnx = mysql.connector.connect(**config)

# 创建一个游标对象
cursor = cnx.cursor()

# 执行一个查询
query = ("SELECT * FROM your_table")
cursor.execute(query)

# 获取查询结果
for (column1, column2) in cursor:
    print("{}, {}".format(column1, column2))

# 关闭游标和连接
cursor.close()
cnx.close()