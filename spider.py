#coding=utf-8
import requests
import threading
import time
import os
import sys
import traceback
from Queue import Queue

MAX_THREAD=200

class Spider:
	def __init__(self):
		self.success=0
		self.url_queue=Queue(maxsize=2000)
	def _check(self):
		while True:
			try:
				if self.url_queue.qsize() !=0:
					url=self.url_queue.get()
					self.total-=1
					r = requests.get('http://%s/console/login/LoginForm.jsp' % (url), timeout=10)
					status = r.content.count('WebLogic')
					if status != 0:
						r = 0
						# print url, 'Exists!!!!!                                                            '
						self.success += 1
						f = open("url_list", 'a')
						f.write(url + '\n')
						f.close()
				else:
					print 'exit'
					break
			except:
				pass
	def read_url_list(self):
		with open(sys.argv[1]) as f:
			for url in f:
				url = url.strip()
				self.url_queue.put(url)
	def blocks(self,files, size=65536):
		while True:
			b = files.read(size)
			if not b: break
			yield b
	def _main(self):
		with open(sys.argv[1]) as f:
			self.total=sum(bl.count("\n") for bl in self.blocks(f))
			print self.total
		t = threading.Thread(target=self.read_url_list)
		t.daemon = True
		t.start()
		time.sleep(5)
		for i in range(0,MAX_THREAD):
			t = threading.Thread(target=self._check)
			t.daemon = True
			t.start()
		while self.url_queue.qsize() !=0:
			sys.stdout.write("Current threads: %d,URLs left: %d,Success:%d                             \r" % (
			threading.active_count(), self.total, self.success), )
			sys.stdout.flush()
			time.sleep(0.3)
		while threading.active_count() > 1:
			sys.stdout.write("Current threads: %d,URLs left: %d,Success:%d                             \r" % (
			threading.active_count(), self.total, self.success), )
			sys.stdout.flush()
			time.sleep(1)
if __name__ == '__main__':
	run=Spider()
	run._main()
