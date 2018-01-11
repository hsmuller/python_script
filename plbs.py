#!/usr/bin/python
import paramiko

ips=['192.168.40.181','192.168.40.180','192.168.40.182','192.168.40.187']
command_rm= 'rm -rf /usr/local/tomcat/webapps/*'
port=22
username="root"
password="####"

def connect(ip):
	s=paramiko.SSHClient() 
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	s.connect(ip,port,username,password)
	return s


def wget(ip):
	s = connect(ip)
	stdin,stdout,sterr=s.exec_command(command_rm)
	if ip[11:] == '180':
		command_wget='wget ftp://192.168.40.170/latest/company.war'
	if ip[11:] == '181':
		command_wget='wget ftp://192.168.40.170/latest/front.war'
	if ip[11:] == '182':
		command_wget='wget ftp://192.168.40.170/latest/customer.war'
	if ip[11:] == '187':
		command_wget='wget ftp://192.168.40.170/latest/platform.war'
	stdin,stdout,sterr=s.exec_command(command_wget)
	result = stdout.read()
	stdin,stdout,sterr=s.exec_command('mv *.war /usr/local/tomcat/webapps/')
	return result

def main():
	for ip in ips:
		result = wget(ip)
		print 'result:'+ result

if __name__ == '__main__':
	main()