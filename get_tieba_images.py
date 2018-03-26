# -*- coding: utf-8 -*-


import os


import argparse
import requests
from bs4 import BeautifulSoup
import re


parser = argparse.ArgumentParser()
parser.add_argument('-p')

args = parser.parse_args()

p = args.p   #输入帖子号


class GetImages():
	def __init__(self, p):
		self.headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) \
				AppleWebKit/537.36 (KHTML, like Gecko) \
				Chrome/47.0.2526.80 Safari/537.36'
			}
		self.url = 'http://tieba.baidu.com/p/{0}?see_lz=1'.format(p)

	def get_resp(self):
		"""获得网页响应"""
		resp = requests.get(self.url, headers=self.headers)
		return resp.text

	def get_soup(self):
		resp = self.get_resp()
		soup = BeautifulSoup(resp, 'html.parser')
		return soup

	def get_name(self):
		"""获得帖子名字"""
		soup = self.get_soup()
		name = soup.find('meta', attrs={'name': 'keywords'})
		content = name['content']
		return content

	def get_img_links(self):
		"""获得每页图片地址"""
		soup = self.get_soup()
		imgtags = soup.find_all('img', class_="BDE_Image")
		imglinks = []
		for imgtag in imgtags:
			imglink = imgtag['src']
			imglinks.append(imglink)
		return imglinks

	def save_image(self, n):
		"""保存图片"""
		name = self.get_name()
		imglinks = self.get_img_links()
		os.mkdir('page{0}'.format(n))
		path = 'page{0}'.format(n)
		os.chdir(path) #转到该文件夹
		for i, j in enumerate(imglinks):
			with open('{0}.jpg'.format(i), 'wb') as file:
				file.write(requests.get(j).content)
		dirpath = os.getcwd()
		parent_path = os.path.split(dirpath)
		os.chdir(parent_path[0])
		print('Page{0} Done.'.format(n))

	def next_page(self):
		pattren = '<a href="(.*?)">下一页</a>'
		resp = self.get_resp()
		result = re.search(pattren, resp)
		if result:
			self.url = 'http://tieba.baidu.com' + result.group(1)
			return self.url   #获得下一页链接
		else:
			self.url = None
		return self.url    #若最后一页则返回无，作为判断

	def main(self):
		n = 1
		while self.url: #利用下一页作为判断
			self.save_image(n)
			n += 1   #表示页数
			self.next_page()
		print('All done.')
getimage = GetImages(p)
getimage.main()
