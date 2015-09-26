#coding=utf-8
import os
import Queue
import requests
import threading
'''
Version 2
Copyright dc3
2015-09-26 18:31
优化多线程控制算法
'''
def check(i,mythreads):
	#os.system("title URLs left: %d" %mythreads.qsize()) #更改窗口标题，如觉得太消耗CPU资源可以注释掉
	try:
		r = requests.get(i+'/login/LoginForm.jsp',timeout=10)
		status=r.content.count('WebLogic')
	except:
		print i,'Timeout'
		status = 0
	if  status !=0: #通过标题判断
		r = 0
		print i,'Exists!!!!!'
		f = open("u.txt", 'a')
		f.write(i+'\n')
		f.close()

def main():
	mythreads = Queue.Queue(maxsize = 0) 
	for i in open("url.txt").readlines():#先将所有线程装入队列，等待取出
		i=i.strip('\n')
		t=threading.Thread(target=check, args=(i,mythreads,))
		t.setDaemon(True)
		mythreads.put(t)
	print 'Total URLs:%d' %mythreads.qsize()
	while True:
		if(threading.active_count() < 100): #判断正在运行的线程数量,如果小于输入值则继续添加线程,默认100线程
			t=mythreads.get() #取出一个线程
			t.start() #加载该线程

if __name__ == '__main__':
	main()		
