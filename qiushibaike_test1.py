# -*- coding: utf-8 -*-
"""
its a web sppider which can gei some information
"""


import re
import requests
from bs4 import BeautifulSoup


class GetQiuishibaike():
	
	def __init__(self):
		self.url = 'https://www.qiushibaike.com/article/120068419'
	
	def get_html(self):
		headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) \
				AppleWebKit/537.36 (KHTML, like Gecko) \
				Chrome/47.0.2526.80 Safari/537.36'
		}
		resp = requests.get(self.url, headers = headers)
		return resp.text

	def subtract_n(self):
		resp = self.get_html()
		resp = re.sub(r'\n|<br>|</br>', '', resp)
		return resp

	def parse_main_messages(self):
		resp = self.subtract_n()
		pattern = re.compile('<div class="author clearfix".*?<h2>(.*)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>', re.S)
		all_messages = re.findall(pattern, resp)
		return all_messages

	def get_comments(self):
		resp = self.get_html()
		soup = BeautifulSoup(resp, 'html.parser')
		pattern = re.compile(r'comment-block clearfix floor-[0-9]+')
		comments = soup.find_all('div', attrs = {'class': pattern})
		replays = []
		for comment in comments:
			replay = comment.find('span', attrs = {'class': 'body'}).get_text()
			replay = str(replay)
			replays.append('%s\n' % replay)
			#replays = replays[::-1]
		return replays

	def print_to_doc(self):
		main_messages = self.parse_main_messages()
		replays = self.get_comments()
		n = 1
		with open('qiushibaike.txt','w') as doc:
			doc.write('楼主：{0[0][0]} \n内容：{0[0][1]}\n赞: {0[0][2]}\n总评论: {0[0][3]}\n\n'.format(main_messages))
			for replay in replays:
				doc.write('%s 楼\n%s' %(n, replay))
				n += 1

qiushibaike = GetQiuishibaike()
qiushibaike.print_to_doc()
