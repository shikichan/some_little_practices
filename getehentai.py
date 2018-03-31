# -*- coding: utf-8 -*-
import os


import requests
import re
from lxml import etree


class GetEHantai():
	def __init__(self):
		self.url = 'https://e-hentai.org/?f_doujinshi=1&f_manga=1&'\
				'f_artistcg=0&f_gamecg=0&f_western=0&f_non-h=0&'\
				'f_imageset=0&f_cosplay=0&f_asianporn=0&f_misc=0&'\
				'f_search=chinese&f_apply=Apply+Filter'
		self.proxies = {
				'http' : 'http://127.0.0.1:1080',
				'https': 'https://127.0.0.1:1080'
				}
		self.headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) \
				AppleWebKit/537.36 (KHTML, like Gecko) \
				Chrome/47.0.2526.80 Safari/537.36'
		}
		self.xpath1 = '//a[contains(@onmouseover, "show_image_pane")]/@href'
		self.xpath2 = '//a[contains(@onmouseover, "show_image_pane")]/text()'
		self.xpath3 = '//*[@id="img"]/@src'
		self.xpath4 = '/html/body/div[1]/div[2]/table[1]/tr/td[13]/a/@href'
		self.xpath5 = '//*[@id="gdt"]/div[1]/div/a/@href'
		#self.titles = self.get_titles()

	def get_html(self):
		resp = requests.get(self.url, proxies=self.proxies, headers=self.headers)
		resp.encoding = 'utf-8'
		resp = resp.text
		html = etree.HTML(resp)
		return html

	def get_links(self):
		html = self.get_html()
		links = html.xpath(self.xpath1)
		return links

	def get_titles(self):
		"""获得漫画名列表"""
		html = self.get_html()
		titles = html.xpath(self.xpath2)
		return titles

	def mkdirs(self):
		"""创建主目录"""
		if os.path.exists('e-hentai'):
			os.chdir('e-hentai')
		else:
			os.mkdir('e-hentai')
			os.chdir('e-hentai')

	def replace_punc(self, title):
		"""替换不符合文件命名规则规则符号"""
		forbid_punc = ['<', '>', ':', '"', '\/', '\|', '\?', '\*' ]
		for punc in forbid_punc:
			title = re.sub(punc, '_', title)
		return title

	def downImg(self, title, href, pagenum, failed_url):
		"""保存漫画页面"""
		try:
			resp = requests.get(
					href, proxies=self.proxies, headers=self.headers, 
					timeout=6
					).content
			with open('num{}.jpg'.format(pagenum), 'wb') as file:
				file.write(resp)
			text = '正保存第{}张图片'.format(pagenum)
			print(text)
		except:
			print('第{}页下载失败'.format(pagenum))
			#failed_url.append(href)
			failed_dict = self.get_dict(title, pagenum, href)
			failed_url.append(failed_dict)


	def get_dict(self, title, pagenum, href):
		"""生成失败链接字典"""
		failed_dict = {}
		failed_dict['title'] = title
		failed_dict['pagenum'] = pagenum
		failed_dict['href'] = href
		return failed_dict

	def mkdir_in_one_page(self, title):
		"""创建同名文件夹"""
		title = self.replace_punc(title)
		if not os.path.isdir(title):
			print('{}\n'.format(title))
			os.mkdir(title)
		os.chdir(title)

	def getcomics(self, title, pagenum, failed_url):
		html = self.get_html()
		href = html.xpath(self.xpath3)[0]   #获取图片路径
		next_page_link = '//*[@id="i3"]/a/@href'
		self.url = html.xpath(next_page_link)[0]   #获取下一页路径
		print(self.url)

		self.downImg(title, href, pagenum, failed_url)

	def return_parent_dir(self):
		"""返回主目录"""
		path = os.getcwd()
		parent_path = os.path.dirname(path)
		os.chdir(parent_path)

	def get_end_p_num(self):
		html = self.get_html()
		href = html.xpath(self.xpath3)[0]
		p_end_xpath = '//*[@id="i2"]/div[1]/div/span[2]/text()'
		p_end = html.xpath(p_end_xpath)[0]
		return p_end

	def downloadimg(self, links, numbers=25):
		"""下载单页里所有的漫画"""
		
		titles = self.get_titles()
		n = 0
		for title in titles:
			pagenum = 1
			if n == numbers:
				print('done')
				break
			title = titles[n]
			self.mkdir_in_one_page(title)   #创建同名漫画文件夹
			self.url = links[n]
			subpage = self.get_html()   #子网页
			self.url = subpage.xpath(self.xpath5)[0]
			print(self.url)   #获取进入漫画阅读界面url
			n += 1
			p_end = self.get_end_p_num()
			print(p_end)
			failed_url = []
			while pagenum <= int(p_end):
				self.getcomics(title, pagenum, failed_url)
				pass
				pagenum += 1
			self.return_parent_dir()
			print(failed_url)
			print('Done.') 

	def get_next_page(self):
		html = self.get_html()
		next_p_href = html.xpath(self.xpath4)[0]
		return next_p_href


	def main(self):
		numbers = int(input('请输入想要获得的漫画数量：'))
		links = self.get_links()   #获得每一页漫画link
		self.mkdirs()   #新建根目录
		self.downloadimg(links, numbers)
		while numbers > 25:
			numbers -= 25
			if numbers > 25:
				self.url = self.get_next_page()
				links = self.get_links()   #获得每一页漫画link
				#self.mkdirs()   #新建根目录
				self.downloadimg(links)
			elif numbers < 25:
				self.url = self.get_next_page()
				links = self.get_links()   #获得每一页漫画link
				#self.mkdirs()   #新建根目录
				self.downloadimg(links, numbers)			





getimgs = GetEHantai()
getimgs.main()