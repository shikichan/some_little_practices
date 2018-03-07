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

	def parse_main_messages(self):
		main_messages = []
		resp = self.get_html()
		soup = BeautifulSoup(resp, 'html.parser')
		author = soup.find('div', attrs = {'class': 'author clearfix'}).find('h2')
		author_name = author.get_text()
		main_text = soup.find('div', attrs = {'class': 'content'}).get_text()
		vote = soup.find('span', attrs = {'class': 'stats-vote'}).find('i', attrs = {'class': 'number'}).get_text()
		total_comments = soup.find('span', attrs = {'class': 'stats-comments'}).find('i', attrs = {'class': 'number'}).get_text()
		all_messages = [
				str(author_name) + '\n', str(main_text), 
				str(vote), str(total_comments)
				]
		for a in all_messages:
			main_messages.append(a)

		return main_messages

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
			doc.write(u'楼主：%s \n内容：%s\n赞: %s\n总评论: %s\n\n' 
						%(main_messages[0], main_messages[1], 
							main_messages[2], main_messages[3]))
		with open('qiushibaike.txt', 'a') as doc:
			for replay in replays:
				doc.write('%s 楼\n%s' %(n, replay))
				n += 1

qiushibaike = GetQiuishibaike()
qiushibaike.print_to_doc()
