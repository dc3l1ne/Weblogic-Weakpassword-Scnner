#coding=utf-8
import requests
import threading
import time
import os
import sys
import traceback

MAX_THREAD=200

class Spider:
	def __init__(self):
		self.success=0
	def _check(self,url):
		try:
			r = requests.get('http://%s/console/login/LoginForm.jsp' % (url), timeout=10)
			status = r.content.count('WebLogic')
			if status != 0:
				r = 0
				print url, 'Exists!!!!!                                                            '
				self.success += 1
				f = open("url_list", 'a')
				f.write(url + '\n')
				f.close()
		except:
			pass
	def blocks(self,files, size=65536):
		while True:
			b = files.read(size)
			if not b: break
			yield b
	def _main(self):
		with open(sys.argv[1]) as f:
			total=sum(bl.count("\n") for bl in self.blocks(f))
			print total
		with open(sys.argv[1]) as f:
			for url in f:
				url = url.strip()
				t = threading.Thread(target=self._check, args=(url,))
				t.setDaemon(True)
				while True:
					if threading.active_count() < MAX_THREAD:
						t.start()
						total-=1
						print "Current threads: %d,URLs left: %d,Success:%d                             \r" % (threading.active_count(), total, self.success),
						break
					else:
						time.sleep(1)
		while threading.active_count() > 1:
			print "Current threads: %d,URLs left: %d,Success:%d                  \r" % (threading.active_count(), total, self.success),
			time.sleep(1)
if __name__ == '__main__':
	run=Spider()
	run._main()
