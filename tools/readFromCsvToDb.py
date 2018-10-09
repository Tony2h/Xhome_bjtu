import pymysql

# encoding:utf8

# 打开数据库连接
db = pymysql.connect("localhost","root","123456","songDB",charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()




with open("playlist_style1.csv") as file:
	for line in file:
		line1=line.split('\n')
		str = line1[0].split(',')
		# SQL 插入语句
		sql = "insert into song(name,singer,style) values (\'{}\',\'{}\',\'{}\')".format(str[0],str[1],str[2])
		print('SQL 插入语句',sql)
		try:
			   # 执行sql语句
			   cursor.execute(sql)
			   # 提交到数据库执行
			   db.commit()
		except:
			   # 如果发生错误则回滚
			   db.rollback()


 
# 关闭数据库连接
db.close()

