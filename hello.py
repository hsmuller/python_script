#  _*_ coding: utf-8 _*_

import wmi
def sys_version(ipaddress, user, password):
    conn = wmi.WMI(computer=ipaddress, user=user, password=password)
    for sys in conn.Win32_OperatingSystem():
        print ("Version:%s" % sys.Caption.encode("UTF8"),"Vernum:%s" % sys.BuildNumber)  #系统信息
        print (sys.OSArchitecture.encode("UTF8") ) # 系统的位数
        print (sys.NumberOfProcesses)  # 系统的进程数
    try:
        filename = r"D:\Java\apache-tomcat-8080\bin\startup.bat"  # 此文件在远程服务器上
        cmd_callbat = r"cmd /c call %s" % filename
        conn.Win32_Process.Create(CommandLine=cmd_callbat)
    except Exception as e:
        print(e)
 
 
if __name__ == '__main__':
    sys_version(ipaddress="192.168.40.180", user="administrator", password="zzsdzfp@123456")