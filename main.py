#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import asyncio
from grayhat import s3
from grayhat import Bucket
#from concurrent.futures import ThreadPoolExecutor

token = input('Enter your grayhatwarfare.com api token: ')
ext = input('Which file extension to search? ').lstrip('.')
print('\nEnter minimum or maximum size of files in Mb: ex. min4000, max0.05')
size = input('Leave empty if none: ')

kwrd = ext.split()
with open('exclude.txt', 'r') as kw:
	for w in kw.read().split(','):
		kwrd += w.split()

bless = Bucket(token, kwrd).get()
# executor = ThreadPoolExecutor(30)

async def proc(bid, st: int = 0):
	global kwrd, bless, size

	for _ in range(100000 // 998):
		warfare = s3(bless.format(bid, st, 990))
		loop = asyncio.get_event_loop()
		run = loop.run_in_executor(None, warfare.files, size, kwrd)
		if not (res := await run) or len(res) < 2:
			break
		elif not (i := res[0]) or st > i:
			break

		st += 990
		with open('results.txt', 'a') as out:
			for loot in res[1:]:
				txt = f"{loot['bid']}  "
				txt += f"{loot['file_url']}  "
				txt += f"{loot['file_size']}\n"
				out.write(txt)
#	if int(bid) % 100 == 0:
#		await asyncio.sleep(2)

async def hack():
	await asyncio.gather(*[proc(bid=Id) for Id in range(1, 91450)])

asyncio.run(hack())

