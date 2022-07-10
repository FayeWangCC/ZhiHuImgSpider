import json
import os.path
import time

import jsonpath
import requests

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
	'referer': 'https://www.zhihu.com/question/26297181',
	'cookie': '_zap=60ec585e-3027-4049-86d2-e37dcf75134f; d_c0="ABARA70vNxWPTvNUZn9ErAQF3Qqd0JdY3so=|1657260754"; _xsrf=8GrLiJQUKpg8caybcjpJ3o5HlkpczBrg; __snaker__id=uIoWwn3imDk9OgNM; _9755xjdesxxd_=32; gdxidpyhxdE=L3PCcG1TtKrYGZE3O9D31G9WIk6ZOtozy%5CxCoptMRz3uJj7NPYAEUopp8bAAzf6UnMCtonmZQ2ZiYhX18ztW%2F%2B7B9ZRGp3XMRkxH87%5Cl0sOUcExiNZrtMg2oRtt%5C3tcpy%2FawdRiRSQvt9Lp%2FVZ5JvdMIvXgSK9%5C%2B2wUhX%2FJHG8pfGS2q%3A1657275867016; YD00517437729195%3AWM_NI=0Zr7zl3pwJw8v8v7wNfkPl3zb4RMbFDGSqIRGFteBPETf4IjpU1P4sxYl37L23ueE0rZoJ7IjxlsjLFo9RivBiPAO5PJfd%2BZZIOJSgTFIWPqdZfrTZnaWvbwUPnt%2FSsjOVE%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee8ebb4db5b69bb9b4669b928ba6d45f839e8a82d44ee995a385e7698bbd00b7c82af0fea7c3b92af486bed8f968f1b0b9abf634b6e8bad8f646a6b5a08db272a2ec9eaee14e88999d92cc5a859abc86c15c878caad5cc62b48bffb1b779bc87a4d4b648f2edbb86c83cb286a1abb643aaa8a494e94886b1f7b3ec7e82b7a0a2ce3f9496aa85aa529a9781abd26d989a87b8d37ba886aa93d752aebf9997e17d9790a295ae59b1b681b7c837e2a3; YD00517437729195%3AWM_TID=l19upPtnrJJFREQVEAeEUrL3cZdJdhQQ; captcha_session_v2=2|1:0|10:1657274967|18:captcha_session_v2|88:SXQydUoyOEd1ODVwTEpGZ3pSQzBxZ1VkZXRMUER1ekxvUDR1d2lBQmZNWUx5WVZId3E2c1VOVlUwaWR3L1lvOA==|864b82b42bb253131435f2979203f1052598d3e423e5434b94d59b749a51ac77; captcha_ticket_v2=2|1:0|10:1657274978|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfNWhzOFkxTUxGREtaSFFLbzZNTXJCOWF3X1IweVpHU0NqSEVzRUxnODkuQldON3BkZlJ3NHpIcEZBZnJIS19uMWRoV1U2ZWo2VmpDNy12anV6bGNTajRJcjk5aDcxek5kY3d5bUcyTlVkQWMxLm9jd2xJOUVMRDV3d0h2ZjVyVERiVENyenJNV3RxRVM0bFh5ckdPU1A3bGZXUy5SZGFWTTdJN3ZlT1NjQWViakdKaDZSLkNpelouQ3JaTXByNkMuMldDeU5vQ0VDQm1WMFdaVlRiZ3ZhV3R6bDhJOF8yR2ZidUE1X0F2bGFCZUhUdmFFNDhuTDF4OEFrZ0h5cnpUeFFrby5rMVYyUm5MaFhwTHM5NUQ2aXg4V2pqWDE4aGtydlRRRG15bjlHOEdJbHlzS3E3TVJobHNNeGhza3FINmkxRGNfOS1fYkpUUHhJTTltUUlLMGROV1RHYndYN2QuYUJQT1pheHFtVllNbmp4N1lvcnpyRHVhY0MuUURaVlFFSVljWGE4OXo1ekJ1UExYOUQxRGZpaXNaanBxR2ZqbWdMbkcua2Z0QUFtRTdnWFFSSHdBcmFUbXY1UDJqMEZaU1NBQlNHdXp3UWdGSUNJbnNzaHgudi5lUmxoVXVDMjVLOVhSZ215UHdzS0NLVmpUc2JycXVQRlFyUGNpMyJ9|0e271acd9da9de5832b985bf94868b3eecf8bcb6f0d0344e5e1532c5fb1a3a40; z_c0=2|1:0|10:1657274978|4:z_c0|92:Mi4xN1R5aUFnQUFBQUFBRUJFRHZTODNGU1lBQUFCZ0FsVk5ZbEMxWXdCcWtqMlpIZFZNRzhTek1XdWx4dXZ4dnZyRW5B|316b9f7c1a3169056690ac0a99bbc3fb091000da39bacd51bb5a5986178c5caf; q_c1=9e27b9f1407441a9803ae8b59bea0a0f|1657274979000|1657274979000; NOT_UNREGISTER_WAITING=1; tst=h; SESSIONID=CfdYTqReH2dpOOiMgkRAmRpawXfvo7am7vhg4T99ijq; KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1657440945|1657440689'
}


# 发送请求获取json数据
def get_data(url):
	# 发送请求获取json数据
	resp = requests.get(url=url, headers=headers)
	content = resp.content
	# 返回json数据
	return content


# 解析json数据
def parse_data(content):
	# 加载json数据
	data = json.loads(content)
	# 解析获取回答数据
	answer_list = jsonpath.jsonpath(data, '$..data')
	# 解析获取下一页请求地址
	answer_next = jsonpath.jsonpath(data, '$..paging..next')[0]
	# 定义一个字典存放答主名称和src列表
	answer_dict = {}
	# 遍历获取每个回答的内容
	for answer in answer_list[0]:
		# 解析获取答主名称
		answer_name = jsonpath.jsonpath(answer, '$..author..name')[0]
		# 解析获取回答内容
		answer_content = str(jsonpath.jsonpath(answer, '$..target..content'))
		# 定义列表存放src路径
		src_list = []
		# 遍历获取内容中所有图片
		while True:
			# 图片src起始位置
			start_index = answer_content.find('data-actualsrc=\"') + 16
			# 图片src结束位置
			end_index = answer_content.find('?source=1940ef5c')
			# 如果能查到结束位置标记则获取src路径避免返回值为-1时的无效查找
			if end_index != -1:
				# 真实图片src路径
				src = answer_content[start_index:end_index]
				# 如果src在列表中不存在且不包含_r则添加到列表中
				if src not in src_list and '_r' not in src and len(src) < 100 and len(src) != 0:
					src = src.replace('_720w', '')
					src_list.append(src)
				# 更新截取后的内容
				answer_content = answer_content[end_index + 17:-1]
			# 如果查不到src结束索引则跳出循环
			else:
				break
		answer_dict[answer_name] = src_list
	# 将存放src的列表和下一页api返回
	return answer_dict, answer_next


def download_img(answer_dict, save_path):
	# 遍历字典获取名称\src列表
	for name, src_list in answer_dict.items():
		# 遍历src列表获取src
		for src in src_list:
			# 发送请求获取图片
			img_resp = requests.get(src, headers=headers)
			# 设置保存路径
			path = save_path + f'{name}'
			# 判断路径是否存在,不存在就创建
			if not os.path.exists(path):
				os.makedirs(path)
			# 保存图片
			with open(f'{path}/{int(time.time())}.jpg', 'wb') as img_f:
				img_f.write(img_resp.content)


if __name__ == '__main__':
	# 设置起始api
	url = 'https://www.zhihu.com/api/v4/questions/26297181/feeds?cursor=e9d89ca6466891518544484e84026815&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id=1657444499711409954'
	save_path = input('请输入要保存的路径,以/结尾:')
	if save_path[-1] != '/':
		save_path = input('没有以/结尾,请重新输入保存路径:')
	while True:
		try:
			# 调用方法获取数据
			content = get_data(url=url)
		except Exception:
			break
		# 调用方法解析图片地址
		answer_dict, url = parse_data(content=content)
		# 调用方法下载图片
		download_img(answer_dict, save_path)
