# -*- coding: utf-8 -*-
import time


import write2db
from getEhentai import GetEHantai as ehentai



get_ehentai = ehentai()
failed_url = []
numbers = int(input('请输入想要获得的漫画数量：'))
links = get_ehentai.get_links()   #获得每一页漫画link
get_ehentai.mkdirs()   #新建根目录e-hentai
failed_url = get_ehentai.downloadimg(links, failed_url, numbers)
while numbers > 25:
	numbers -= 25
	if numbers > 25:
		get_ehentai.url = get_ehentai.get_next_page()
		links = get_ehentai.get_links()   #获得每一页漫画link
		#get_ehentai.mkdirs()   #新建根目录
		failed_url = get_ehentai.downloadimg(links)
	elif numbers < 25:
		get_ehentai.url = get_ehentai.get_next_page()
		links = get_ehentai.get_links()   #获得每一页漫画link
		#get_ehentai.mkdirs()   #新建根目录
		failed_url = get_ehentai.downloadimg(links, numbers)
if failed_url:
	write2db.write_in_failedDB(failed_url)
	# time.sleep(20)
	write2db.redownload(get_ehentai)
else:
	print('下载完毕')
