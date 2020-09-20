#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests, json, re

from random import sample
from typing import List



class ForbiddenAccess(Exception):
	pass


class Bucket():

	def __init__(self, api_k: str, ext: List[str] = []):
		self.api = api_k
		self.ext = ext

	def get(self):
		url = 'https://buckets.grayhatwarfare.com/api/v1'
		url += '/bucket/{}/files/{}/{}'
		url += f'?access_token={self.api}&keywords='
		for ex in (n := self.ext):
			if not ex.startswith('-'):
				if n.index(ex) > 0:
					continue
			url += f'{ex}%20'
		return url


class s3:

	def __init__(self, url: str):
		self.pl = url
		self.list = []

	def search(self):
		try:
			resp = requests.get(self.pl, timeout=20)
		except:
			return False
		if resp.status_code == 200:
			return resp.json()
		elif resp.status_code == 401:
			raise ForbiddenAccess('Check your access token.')
		else:
#			print(f'[Code: {resp.status_code}] Connection error..')
			return False

	def files(self, size: float = None, ext: List[str] = []):
		print(f"Bucket ID: {self.pl.split('bucket/')[1].split('/')[0]} \
/ 91450", end="\r")
		Files = self.search()
		if not Files:
			return False
		self.list.append(int(Files['results']))
		for file in Files['files']:
			buc = {}
			buc['fid'] = file['id']
			buc['bid'] = file['bucketId']
			buc['bucket'] = file['bucket']
			buc['filename'] = file['filename']
			buc['file_path'] = file['fullPath']
			buc['file_url'] = file['url']
			mb = float(f"{int(file['size']) / 1048576}")
			buc['file_size'] = f'{int(mb)} Mb'
			if size:
				if mb > float(size):
					self.trash(file['url'])
					continue
			if (fl := file['filename'].split('.'))[-1] != ext[0]:
				if fl[-1] != (str(ext[0]) + '~'):
					if len(fl) < 2 or fl[-2] != ext[0]:
						self.trash(file['url'])
						continue
			for _ in (_x := sample(ext[1:], len(ext) -1)):
				chk = file['url'].split('//')[1]
				if _.lstrip('-') in re.split(r'[.-/-_\s]\s*', chk):
					self.trash(file['url'])
					break
				elif _x[-1].endswith(_):
					self.list.append(buc)
		return self.list

	def trash(self, url):
		with open('trash.txt', 'a') as out:
			out.write(f'{url}\n')

