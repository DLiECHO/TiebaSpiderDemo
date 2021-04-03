import requests

class test():
    def __init__(self):
        self.post_url = 'https://tieba.baidu.com/f?kw=hpv&ie=utf-8&pn='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Mobile Safari/537.36'
        }

    def get_url_list(self):
        '''记录贴吧前272页的地址（截止2021年4月2日上午共272页）'''
        list = []
        for i in range(272):
            list.append(self.post_url+str((i-1)*50))
        return list

    def get_post(self, url):
        '''访问所记录的网址'''
        response = requests.get(url=url, headers=self.headers)
        return response.content.decode()

    def save_html(self, cnotent, page_num):
        '''将爬取的数据存入文件当中去'''
        filename = "document.txt"
        with open(filename, "w", encoding='utf-8')as f:
            f.write(cnotent)

    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            cnotent = self.get_post(url)
            page_num = url_list.index(url)+1
            self.save_html(cnotent, page_num)

tieba_spider = test()
tieba_spider.run()