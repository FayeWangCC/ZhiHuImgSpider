import os.path
import random
import time

import requests
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By


# 使用requests获取图片并保存到本地
def save_image(src, save_path):
	# 处理图片src地址获取高清图片地址
	current_src = src.replace('_720w.jpg?source=1940ef5c', '.jpg')

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
		'referer': 'https://www.zhihu.com/'
	}

	# 打开src获取相应
	resp = requests.get(current_src, headers=headers)

	# 判断目录是否存在
	if not os.path.exists(save_path):
		# 如果不能存在就创建
		os.mkdir(save_path)
	# 图片名称以时间戳命名
	img_title = str(int(time.time())) + '.jpg'
	# 保存图片
	with open(f'{save_path}/{img_title}', 'wb') as f_img:
		# 写入二进制文件内容
		f_img.write(resp.content)
	print(f'图片保存成功\n\n{img_title}')


# 使用selenium获取图片地址
def get_img_src(question_url, save_path):
	# 设置selenium参数
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('lang-zh_CN.utf-8')
	useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'
	chrome_options.add_argument('User-Agent=' + useragent)
	# 创建浏览器对象
	driver = webdriver.Chrome(chrome_options=chrome_options)
	# 设置浏览器窗口大小
	driver.set_window_size(1366, 768)
	# 打开url地址
	driver.get(question_url)
	# 等待页面3秒，加载出登录框
	time.sleep(3)
	# 点击登录框的关闭按钮
	driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/button').click()

	# 定义每次滚动屏幕的距离
	height = 1000
	# 定义列表存储图片地址
	img_list = []
	# 循环滚动屏幕获取图片地址
	while True:
		# 滚动屏幕到指定位置
		driver.execute_script(f'scrollTo(0,{height})')
		try:
			# 获取回答内容中的图片对象列表
			el_img_list = driver.find_elements(By.XPATH, '//div[@class="List-item"]//span//figure/img')

			# 从图片对象列表中获取图片
			for el_img in el_img_list:
				# 从图片对象中获取图片src属性值
				src = str(el_img.get_attribute('src'))
				# 根据图片src属性值判断是否为目标图片src
				if 'data:image/svg+xml' not in src:
					# 判断该src在列表中是否存在，如果不存在就添加
					if src not in img_list:
						img_list.append(src)
						# 调用方法下载图片
						save_image(src, save_path)
		# 页面重新加载新内容时会出现无法获取到指定对象的异常
		except StaleElementReferenceException:
			time.sleep(5)
			continue
		# 等待1秒
		time.sleep(1)
		# 将滚动屏幕的距离增加
		height += random.randint(768, 1000)

		try:
			# 获取结束标志‘写内容按钮’
			if driver.find_element(By.XPATH, '//div[@class="Card"]/a/button').text == '写内容':
				break
		except NoSuchElementException:
			continue


if __name__ == '__main__':
	# 获取问题ID
	question_id = input('请输入知乎问题ID:')
	# 拼接问题链接地址
	question_url = 'https://www.zhihu.com/question/' + question_id
	# 设置图片保存目录
	save_path = f'./{question_id}'
	# 调用方法获取图片地址
	get_img_src(question_url=question_url, save_path=save_path)
