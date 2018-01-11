#  _*_ coding: utf-8 _*_
#!/usr/bin/python 

import paramiko
import threading
from sys import argv
import re
from time import sleep
import sys


ips=['192.168.40.181','192.168.40.180','192.168.40.182','192.168.40.187']
port=22
username="root"
password="123123"
command_status = "ps aux |grep tomcat | grep -v grep | wc -l"
command_start = '/usr/local/tomcat/bin/startup.sh'
command_stop = '/usr/local/tomcat/bin/shutdown.sh'
command_statu = 'netstat -anput |grep 8080 |wc -l'
command_kill_num = "ps aux |grep tomcat|grep -v grep|awk '{print $2}'"

def connect(ip):
	s=paramiko.SSHClient() 
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	s.connect(ip,port,username,password)
	return s

def startup(ip):
	s = connect(ip)
	stdin,stdout,sterr=s.exec_command(command_status)
	num = stdout.read()
	num = int(re.match('(\d+)',num).group(1))
	if num != 0:
		print '%s tomcat has started!' % ip
		s.close()
		return
	if num == 0:
		s.exec_command(command_start)
		print '%s starting tomcat' % ip
		sleep(3)
		stdin,stdout,sterr=s.exec_command(command_status)
		num = int(re.match('(\d+)',stdout.read()).group(1))
		if num == 1:
			print '%s tomcat started' % ip
		s.close()
		return

def shutdown(ip):
	s = connect(ip)
	stdin,stdout,sterr=s.exec_command(command_status)
	num = stdout.read()
	num = int(re.match('(\d+)',num).group(1))
	if num > 1:
		print '%s server error' % ip
		s.close()
		return
	if num == 1:
		s.exec_command(command_stop)
		print '%s stoping tomcat' % ip
		sleep(3)
		stdin,stdout,sterr=s.exec_command(command_statu) 
		num = stdout.read()
		num = int(re.match('(\d+)',num).group(1))
		if num == 0:
			stdin,stdout,sterr=s.exec_command(command_status)
			num = stdout.read()
			num = int(re.match('(\d+)',num).group(1))
			if num == 0:
				print ip + ' tomcat has stoped'
				s.close()
				return
			if num == 1:
				stdin,stdout,sterr=s.exec_command(command_kill_num)
				kill_num = re.match('(\d+)',stdout.read()).group(1)
				s.exec_command('kill '+kill_num)
				stdin,stdout,sterr=s.exec_command(command_statu)
				num1 = int(re.match('(\d+)',stdout.read()).group(1))
				stdin,stdout,sterr=s.exec_command(command_status)
				num2 = int(re.match('(\d+)',stdout.read()).group(1))
				s.close()
				if num1 == 0 and num2 ==0:
					print '%s tomcat has stoped' % ip
					return
				else:
					print '%s server error' % ip
					return
	if num == 0:
		print 'tomcat not running'
		s.close()
		return


def restart(ip):
	s = connect(ip)
	stdin,stdout,sterr=s.exec_command(command_status)
	num = stdout.read()
	num = int(re.match('(\d+)',num).group(1))
	if num > 1:
		print '%s server error' % ip
		s.close()
		return 'error'
	if num == 1:
		s.exec_command(command_stop)
		print '%s stoping tomcat' % ip
		sleep(3)
		stdin,stdout,sterr=s.exec_command(command_statu) 
		num = stdout.read()
		num = int(re.match('(\d+)',num).group(1))
		if num == 0:
			stdin,stdout,sterr=s.exec_command(command_status)
			num = stdout.read()
			num = int(re.match('(\d+)',num).group(1))
			if num == 0:
				print ip + ' tomcat has stoped'
			if num == 1:
				stdin,stdout,sterr=s.exec_command(command_kill_num)
				kill_num = re.match('(\d+)',stdout.read()).group(1)
				s.exec_command('kill '+kill_num)
				stdin,stdout,sterr=s.exec_command(command_statu)
				num1 = int(re.match('(\d+)',stdout.read()).group(1))
				stdin,stdout,sterr=s.exec_command(command_status)
				num2 = int(re.match('(\d+)',stdout.read()).group(1))
				if num1 == 0 and num2 ==0:
					print '%s tomcat has stoped' % ip
				else:
					print '%s server error' % ip
					return 'error'
	if num == 0:
		print 'tomcat not running'
	stdin,stdout,sterr=s.exec_command(command_status)
	num = stdout.read()
	num = int(re.match('(\d+)',num).group(1))
	if num != 0:
		print '%s tomcat has started!' % ip
		s.close()
		return
	if num == 0:
		s.exec_command(command_start)
		print '%s starting tomcat' % ip
		sleep(3)
		stdin,stdout,sterr=s.exec_command(command_status)
		num = int(re.match('(\d+)',stdout.read()).group(1))
		if num == 1:
			print '%s tomcat started' % ip
		s.close()
		return

#def main():
	# comm = argv[1]
	# if comm == 'start':
	# 	command = startup
	# if comm == 'stop':
	# 	command = shutdown
	# if comm == 'restart':
	# 	command = restart
	# thread_list == []
	# for i in range(len(ips)):
	# 	t = threading.Thread(target=command,args=(ips[i])
	# 	thread_list.append(t)
#	for i in range(len(ips)): 
#		thread_list[i].start()


for ip in ips:
	if argv[1] == 'start':
		startup(ip)
	if argv[1] == 'stop':
		shutdown(ip)	
	if argv[1] == 'restart':
		restart(ip)

#	main()
