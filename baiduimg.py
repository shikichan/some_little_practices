# -*- coding: utf-8 -*-

import requests
import urllib.parse
import time
import random
import os


#parser = argparse.ArgumentParser()
#parser.add_argument('-k')

#args = parser.parse_args()

#k = args.k   #输

class BaiduImg():
	def __init__(self):
		self.pn = input('请输入想获得的图片张数，30的整数倍：')
		self.k = str(input('请输入关键字：'))

		self.n = 1
		self.a = 0

	def trans(self):
		k = urllib.parse.quote(self.k)
		return k

	def get_url(self):
		timerandom = random.randint(100,999)
		nowtime = int(time.time())
		stamp = str(nowtime) + str(timerandom)   #url最后的时间戳组成
		transk =  self.trans()
		url = 'https://image.baidu.com/search/acjson?tn=resultjson_com'\
				'&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2'\
				'&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1'\
				'&word={0}&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2'\
				'&qc=&nc=1&fr=&step_word={0}'\
				'&pn={1}&rn=30&gsm=1e&{2}='.format(transk, self.pn, stamp)   #pn为不同的js包
		return url

	def get_json(self, url):
		resp = requests.get(url)
		respjs = resp.json()
		return respjs

	def save_one_img(self, imgsouce):
		resp = requests.get(imgsouce).content
		with open('num{0}.jpg'.format(self.n), 'wb') as file:
			file.write(resp)
		print('保存第{0}张图片'.format(self.n))

	def save_imgs(self, respjs):
		data = respjs['data']
		imgsouces = []
		num = 0
		while num < 30:
			imgsouce = data[num]['middleURL']
			print('获得第{0}张图片地址：{1} '.format(self.n, imgsouce))
			self.save_one_img(imgsouce)
			self.n += 1
			num += 1
		print('共获得{0}'.format(self.n - 1))

	def newdir(self):
		os.mkdir('{0}'.format(self.k))
		os.chdir('{0}'.format(self.k))

	def once_main(self):
		url = self.get_url()
		respjs = self.get_json(url)
		self.save_imgs(respjs)

	def main(self):
		self.newdir()
		while self.a < int(self.pn):
			self.once_main()
			self.a += 30
		print('Done.')

get_img = BaiduImg()
get_img.main()

