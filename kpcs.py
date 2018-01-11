# -*- coding:utf-8 -*-

from selenium import webdriver
from time import sleep
from datetime import datetime as dt
import threading
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import cs_db


def WebDriver(url,data):
	driver = webdriver.Firefox()
#	driver = webdriver.PhantomJS()
	driver.get(url)
	sleep(2)
	while True:
		try:
			if driver.find_element_by_id("buyerName"):
					driver.find_element_by_id("buyerName").clear()
					driver.find_element_by_id("buyerName").send_keys(data[0])
					driver.find_element_by_id("taxno").clear()
					driver.find_element_by_id("taxno").send_keys(data[1])
					driver.find_element_by_id("email").clear()
					driver.find_element_by_id("email").send_keys(data[2])
					driver.find_element_by_id("mobile").clear()
					driver.find_element_by_id("mobile").send_keys(data[3])
					driver.find_element_by_tag_name("button").click()
					time_1 = dt.now()
					break
		except NoSuchElementException:
			driver.get(url)
			sleep(2)
	print time_1
	while True:
		try:
			if driver.find_element_by_id('diva'):
				time_2 = dt.now()
				print time_2
				break
		except :
			sleep(0.2)
	time = (time_2 - time_1).seconds
	print time
	driver.quit()
	return time

def get_list():
	#url_list = ['http://192.168.40.181:8080/CodePlatform/CodePlatformServlet?taxNo=91110101999999002X&orderId=sigjggggIIJKsosoklsilgklsjqqokqho']
	orderID_list = []
	f = open('C:/Users/Admin/Desktop/result.txt')
	for i in range(26):
	    orderID_list.append(f.readline().strip())
	url = 'http://192.168.40.181:8080/front/CodePlatformServlet?taxNo=91110101999999002X&orderId='
	url_list=[]
	for i in orderID_list:	
		url_list.append(url+i)
	data_list = {}
	a_list = []
	phone_list = ['15010121476','13521350194','13693572876','15116978572','13661335405','18201646536']
	for i in xrange(6):
	    a = chr(i+ord('A'))
	    data_list[i]=[a,'123451234512345123','412423777@qq.com']
	    if len(data_list[i]) < 4:
	    	data_list[i].append(phone_list[i])
	return data_list,url_list

def thread_create(data_list,url_list,start_num=0,stop_num=5):
	threads = []
	for i in range(start_num,stop_num):
		print url_list[i]
		print data_list[i]
		proc = threading.Thread(target=WebDriver,args=(url_list[i],data_list[i]))
		threads.append(proc)
	for t in threads:
		t.start()
	for t in threads:
		t.join()

def main():
	cs_db.delete_db()
	data_list,url_list = get_list()
	thread_create(data_list,url_list,0,3)

if __name__ == '__main__':
	main()
