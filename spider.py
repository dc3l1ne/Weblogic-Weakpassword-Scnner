#coding=utf-8
import requests
import threading
import time
import os
import sys

MAX_THREAD=100

class Spider:
	def __init__(self):
		self.success=0
	def _check(self,url):
		try:
			r = requests.get('http://%s/console/login/LoginForm.jsp' % (url), timeout=10)
			status = r.content.count('WebLogic')
			if status != 0:
				r = 0
				print i, 'Exists!!!!!                                                            '
				self.success += 1
				f = open("url_list", 'a')
				f.write(i + '\n')
				f.close()
		except:
			pass
	def blocks(files, size=65536):
		while True:
			b = files.read(size)
			if not b: break
			yield b
	def _main(self):
		with open(sys.argv[1]) as f:
			total=sum(bl.count("\n") for bl in self.blocks(f))
			for url in f:
				url = url.strip()
				t = threading.Thread(target=check, args=(url,))
				t.setDaemon(True)
				while True:
					if threading.active_count() < MAX_THREAD:
						t.start()
						total-=1
						print "Current threads: %d,URLs left: %d,Success:%d\r" % (threading.active_count(), total, self.success),
						break
					else:
						time.sleep(1)

if __name__ == '__main__':
	main()
