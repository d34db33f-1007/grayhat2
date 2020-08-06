#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys, re
import requests, json

from typing import List



class ForbiddenAccess(Exception):
	pass


class Build:

	def Bucket(api_k: str, b_id: str, start = 0, stop=None, ext: List[str] = []):
		buck = 'https://buckets.grayhatwarfare.com/api/v1'
		buck += f'/bucket/{b_id}/files'
		buck += f'/{start}/{stop}' if stop else f'/{start}'
		buck += f'?access_token={api_k}'
		if ext and 0 < len(ext) < 5:
			with open('exclude.txt', 'r') as negative:
				for trash in negative.read().split(','):
					if trash.startswith('-'):
						ext += trash.split()
		if len(ext) > 0:
			buck += f'&keywords='
			e = '%20' if len(ext) > 1 else ''
			for ex in ext:
				n = ext.index(ex)
				if n > 0 and not ex.startswith('-'):
					continue
				buck += f'{ex}{e}' if n < (len(ext) -1) else f'{ex}'
		return buck


class s3:

	def __init__(self, url: str):
		self.pl = url
		self.list = []

	def search(self):
		try:
			resp = requests.get(self.pl)
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
		self.list.append(f"{Files['results']}")
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
				if mb < float(size):
					self.trash(file['url'])
					continue
			if re.split(r'[.-/-_\s]\s*', file['filename'])[-1] != ext[0]:
				self.trash(file['url'])
				continue
			for x in ext[1:]:
				x = x.replace('-', '') if x.startswith('-') else x
				chk = file['url'].split('//')[1]
				if x in re.split(r'[.-/-_\s]\s*', chk):
					if buc:
						self.trash(file['url'])
						buc = None
			if buc:
				self.list.append(buc)
		return self.list

	def trash(self, url):
		with open('trash.txt', 'a') as out:
			out.write(f'{url}\n')

