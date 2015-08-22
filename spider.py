#coding=utf-8
import sys
import requests
import threading
def check(i):
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
	for i in open(sys.argv[1]).readlines():
		i=i.strip('\n')
		while threading.active_count()>200:
			pass
		t = threading.Thread(target = check,args=(i,))
		t.start()

if __name__ == '__main__':
	main()
