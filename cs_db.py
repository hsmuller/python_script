import pymysql

def delete_db():
	conn = pymysql.connect(host='192.168.40.180',port=3306,user='root',passwd='####',db='####',charset='utf8')
	cursor = conn.cursor()

	deleteRow2 = cursor.execute('delete from o_order_item where 1=1 ')
	print 'delete ' + str(deleteRow2) + 'hang'
	deleteRow1 = cursor.execute('delete from  o_order where 1=1')
	print 'delete ' + str(deleteRow1) + 'hang'

	conn.commit()  
	cursor.close()  
	conn.close()

if __name__ == '__main__':
	delete_db()