import requests
import time
import pymysql
from bs4 import BeautifulSoup

all_language = ['C%2B%2B','Java','Python','R语言', 'Go', 'Matlab', 'Scala', 'VB.NET', 'SQL',
                'Objective-C', 'C', 'Ruby', 'PHP', '汇编', 'C%23']
all_company = ['字节跳动', '阿里巴巴', '华为', '腾讯', '金山', '百度' ,'京东', '滴滴出行', '小米', '360'\
                '美团', '网易', '拼多多', '携程', '新浪', '苏宁易购', '快手', '唯品会', '陆金所', '科大讯飞'\
                '58', '汽车之家', '爱奇艺', '链家网', '哔哩哔哩', '斗鱼', '迅雷']


class spider:
    def __init__(self):
        self.data = []
        self.company = []
        self.job = []
        self.money = []
        self.place = []
        self.url = ''
        self.headers = {}
        self.status = 0
        self.max_money = 0
        self.max_moneyjob = ''
        self.min_money = 10000
        self.min_moneyjob = ''
        self.average = 0
        self.count = 0

    def get_it(self):   #获取记录的基本信息
        self.headers[
            'user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/60.0.3112.78 Safari/537.36 '
        res = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        self.status = res.status_code
        table_company = soup.find('div', class_="job-list").find_all('a', target='_blank')
        table_job = soup.find('div', class_='job-list').find_all('div', class_='job-title')
        table_money = soup.find('div', class_='job-list').find_all('span', class_='red')
        table_place = soup.find('div', class_='job-list').find_all('p')
        i = 0
        while i < len(table_place):
            temp = 0
            for j in table_place[i].descendants:
                if temp == 0:
                    self.place.append(j)
                    temp += 1
            i += 3
        i = 1
        while i < len(table_company):
            self.company.append(table_company[i].text)
            self.job.append(table_job[int((i - 1) / 3)].text)
            self.money.append(table_money[int((i - 1) / 3)].text)
            i += 3

    def gather(self):
        i = 0
        while i < len(self.company):
            temp = [self.company[i], self.job[i], self.money[i], self.place[i]]
            self.data.append(temp)
            i += 1

    def money_trans(self):  #计算最低薪资，最高薪资和平均薪资
        all_money = 0
        for i in range(len(self.money)):
            now_company_temp = now_company
            j = 0
            temp1 = ''
            temp2 = ''
            if now_company_temp == '字节跳动':
                now_company_temp = '今日头条'
            elif now_company_temp == '阿里巴巴':
                now_company_temp = '阿里'
            elif now_company_temp == '哔哩哔哩':
                now_company_temp = 'bilibili'
            if int(self.company[i].find(now_company)) == -1 and self.company[i].find(now_company_temp) \
                    or int(self.job[i].find('产品') != -1) or int(self.job[i].find('C端') != -1) or int(self.job[i].find('编辑') != -1) :
                continue
            self.count += 1
            while self.money[i][j] != '-':
                temp1 += self.money[i][j]
                j += 1

            if int(temp1) < self.min_money:
                self.min_money = int(temp1)
                self.min_moneyjob = self.job[i]
            j += 1
            while self.money[i][j] != 'K':
                temp2 += self.money[i][j]
                j += 1
            all_money += int(temp1) + (int(temp2) - int(temp1)) * 0.1
            if int(temp2) > self.max_money:
                self.max_money = int(temp2)
                self.max_moneyjob = self.job[i]
        if self.count != 0:
            all_money /= self.count
            self.average = all_money

    def renew(self):
        self.data = []
        self.company = []
        self.job = []
        self.money = []
        self.place = []
        self.headers = {}
        self.status = 0
        self.max_money = 0
        self.max_moneyjob = ''
        self.min_money = 10000
        self.min_moneyjob = ''
        self.average = 0
        self.count = 0


def set_url(page):
    now_url = spider.url
    new = 'page='+str(page)+'&ka=page-'+str(page)
    now_url = now_url[:int(now_url.find('page'))]
    now_url += new
    spider.url = now_url


if __name__ == '__main__':
    spider = spider()
    for now_company in all_company:
        for now_language in all_language:
            print(now_language)
            Min_money = []
            Max_money = []
            Min = 10000
            Min_job = ''
            Max = 0
            Max_job = ''
            All_money = 0
            count = 0
            spider.url = 'https://www.zhipin.com/c100010000/?query='+now_language+'+'+now_company+'&page=1&ka=page-1'
            for i in range(1,9):
                print(spider.url)       #输出当前爬取网页的url
                set_url(i)
                spider.get_it()
                spider.gather()
                spider.money_trans()
                Min_money.append(spider.min_money)
                Max_money.append(spider.max_money)
                All_money += spider.average*spider.count
                count += spider.count
                if spider.min_money < Min:
                    Min = spider.min_money
                    Min_job = spider.min_moneyjob
                if spider.max_money > Max:

                    Max = spider.max_money
                    Max_job = spider.max_moneyjob
                    print(Max_job)
                spider.renew()
                time.sleep(60)
            if count != 0:
                Average = int(All_money/count)
            else:
                Average = 0
                Min = 0
            if now_language == 'R语言':
                now_language = 'R'
            elif now_language == '汇编':
                now_language = 'Assembly'
            elif now_language == 'C%2B%2B':
                now_language = 'C++'
            elif now_language == 'C%23':
                now_language = 'C#'

            #输出本轮结果
            print("当前语言名: ", now_language,", 当前公司名: ", now_company)
            print("平均薪资: ", Average, ", 最高薪资: ", Max, ", 最高薪资岗位: ", Max_job, ", 最低薪资: ", Min, ", 最低薪资岗位: ", Min_job)

            time.sleep(120)
