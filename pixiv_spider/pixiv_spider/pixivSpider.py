import requests
from lxml import etree
import uuid
import time
import json

headers = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "accept-language": "zh-CN,zh;q=0.9",
    "referer": "https://www.pixiv.net/",
}

# 获取主页列表
def get_pixiv_index(page):
    base_url = 'https://www.pixiv.net'
    url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p={}&format=json'.format(page)
    resp = requests.get(url,headers=headers).json()
    contents = resp['contents']
    img_list = []
    for img_data in contents:
        img_list.append({
            'pid':img_data['illust_id']
        })
    return img_list

# 获取详情页json及图片URL
def get_detail_json(img_list):
    for img_data in img_list:
        pid = img_data['pid']
        url = 'https://www.pixiv.net/ajax/illust/{}/pages?lang=zh'.format(pid)
        resp = requests.get(url,headers= headers).json()
        body = resp['body']
        urls  = []
        for img_url in body:
            urls.append({
                'original':download_img(img_url['urls']['original'],pid),
                'regular':img_url['urls']['original'],
                'small':img_url['urls']['original'],
                'thumb_mini':img_url['urls']['original'],
            })

# 下载图片
def download_img(url,pid):
    resp = requests.get(url,headers=headers).content
    with open('./image/{}.jpg'.format(uuid.uuid4()),'wb')as f:
        f.write(resp)
    print('Pid:{}下载完成'.format(pid))

# 调度
def run():
    page = input('要爬取第几页：')
    img_list = get_pixiv_index(page)
    get_detail_json(img_list)


if __name__ == '__main__':
    run()
