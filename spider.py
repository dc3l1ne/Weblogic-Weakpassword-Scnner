#coding=utf-8
import requests
import threading
import time
import os
import sys

def check(i,total):
	global eu
	try:
		r = requests.get('http://%s:%s/console/login/LoginForm.jsp'%(i),timeout=10)
		status=r.content.count('WebLogic')
		if status !=0:
			r = 0
			print i,'Exists!!!!!                                                            '
			eu+=1
			f = open("u.txt", 'a')
			f.write(i+'\n')
			f.close()
	except:
		print i,'Timeout'

def main():
	global eu
	eu = 0
	total=len(open(sys.argv[1],'rU').readlines())
	print 'Total URLs:%d' %total
	for i in open("url.txt").readlines():
		i=i.strip('\n')
		t=threading.Thread(target=check, args=(i,total))
		t.setDaemon(True)
		total-=1
		while True:
			if(threading.active_count() == 1 and total == 0 ):
				print 'All Done at %s' %time.strftime("%Y-%m-%d[%H.%M.%S]")
				break
			elif (threading.active_count() < 200):
				if (total == 0):
					time.sleep(10)
				else:
					print "title Spider,Current threads: %d,URLs left: %d,URLs exists:%d" %(threading.active_count(),total,eu)),
					t.start()
					break


if __name__ == '__main__':
	main()
