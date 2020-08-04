#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import asyncio
from grayhat import s3
from grayhat import Build as bl
#from concurrent.futures import ThreadPoolExecutor

class Brute:

	def __init__(self):
		self.token = input('Enter your grayhatwarfare.com api token: ')
		self.in1 = input('Which file extension to search? ex. zip: ')
		if self.in1.startswith('.'):
			self.in1 = self.in1.replace('.', '')
		print('\nEnter minimum size of files in Mb: ex. 4000, 0.05')
		self.in2 = input('Enter 0 if none: ')
		self.extensions = self.in1.split()
		self.keywords = self.extensions
		with open('exclude.txt', 'r') as kw:
			for w in kw.read().split(','):
				if w.startswith('-'):
					self.keywords += w.split()
#		self.executor = ThreadPoolExecutor(30)

	async def proc(self, bid, st: int = 0):
		for __ in range(100000 // 998):
			bless = bl.Bucket(api_k = self.token, b_id=bid, start=st, stop=998, ext=self.extensions)
			warfare = s3(bless)
			loop = asyncio.get_event_loop()
			run = loop.run_in_executor(None, warfare.files, float(self.in2), self.keywords) # L24
			res = await run
			if not res:
				break
			elif res and len(res) < 2:
				break
			elif st > int(res[0]) or int(res[0]) == 0:
				break
			else:
				st += 998
				with open('results.txt', 'a') as out:
					for f in res[1:]:
						txt = f"{f['bid']}  {f['file_url']}  {f['file_size']}\n"
						out.write(txt)
		if int(bid) % 100 == 0:
			await asyncio.sleep(2)

	async def hack(self):
		await asyncio.gather(*[self.proc(bid=Id) for Id in range(1, 91450)])


if __name__ == '__main__':
	blazing = Brute()
	asyncio.run(blazing.hack())

