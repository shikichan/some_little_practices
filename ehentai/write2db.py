# -*- coding: utf-8 -*-


import os


import re
import requests
from pymongo import MongoClient


def write_in_savedDB(title):
	"""把成功下载的漫画目录写入数据库"""
	client = MongoClient('localhost', 9000)
	db = client.ehentai
	posts = db.ehentai
	keyword = {'title': '{}'.format(title)}
	search_result = posts.find_one(keyword)
	if search_result:
		return 0    #停止写入和下载漫画
	else:
		posts.insert_one(keyword)
		return 1   #继续写入

def write_in_failedDB(failed_url):
	"""把失败漫画页面链接列表写入数据库"""
	client = MongoClient('localhost', 9000)
	db = client.ehentai
	posts = db.failed
	posts.insert_many(failed_url)
	print('写入失败链接完毕.')

def redownload(get_ehentai):
	client = MongoClient('localhost', 9000)
	db = client.ehentai
	posts = db.failed
	results = posts.find()
	for result in results:
		title = result['title']
		href = result['href']
		pagenum = result['pagenum']
		titleB = get_ehentai.replace_punc(title)		
		path = '{}'.format(titleB)
		img_name = 'num{}.jpg'.format(pagenum)
		os.chdir(path)
		try:
			resp = requests.get(
					href, proxies=get_ehentai.proxies, 
					headers=get_ehentai.headers, 
					timeout=10
					).content
			with open(img_name, 'wb') as file:
				file.write(resp)
			# posts.remove({'href': href})
			text = '{}: 第{}页重新下载已完成'.format(titleB, pagenum)
			print(text)
		except:
			print('认命吧！！！')
		get_ehentai.return_parent_dir()


if __name__ == '__main__':
	from getehentai_v2 import GetEHantai as ehentai
	get_ehentai = ehentai()
	redownload(get_ehentai)
# for result in results:
# 	pr = '{}\n'.format(result)
# 	print(pr)
