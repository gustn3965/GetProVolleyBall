from selenium import webdriver
import time
import pandas as pd
import re


class VolleyBall():
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('headless')
        self.option.add_argument('hide_console')
        self.driver = webdriver.Chrome("C:/Users/Administrator/PycharmProjects/PracticeDesinApi/chromedriver.exe",
                                       options=self.option)

    def getData(self, url, progressBar):
        self.dict = {'date': [], 'sex': [], 'visitTeam': [], 'homeTeam': [], 'playTimes': [], 'stageName': [],
                     'volume': [], 'visitScore': [], 'homeScore': []}
        self.driver.get(url)
        time.sleep(2)
        wrp_lst = self.driver.find_element_by_class_name('wrp_lst')
        tbody = wrp_lst.find_element_by_tag_name('tbody')
        trs = tbody.find_elements_by_tag_name('tr')

        rcv_count = 0

        addressList = []
        for tr in trs:
            a_s = tr.find_elements_by_tag_name('a')
            for a in a_s:
                real_a = a.get_attribute('href')
                respond = re.search('game-summary', real_a)
                if respond:
                    addressList.append(real_a)

        progressBar.setMinimum(rcv_count)
        progressBar.setMaximum(len(addressList))
        print("해당 날짜의 Maximum : ", len(addressList), " 개")

        for address in addressList:
            rcv_count += 1
            print(rcv_count, "개 받는 중 ")
            progressBar.setValue(rcv_count)
            driverDetail = webdriver.Chrome("C:/Users/Administrator/PycharmProjects/PracticeDesinApi/chromedriver.exe",
                                            options=self.option)
            driverDetail.get(address)

            lst_recentgame = driverDetail.find_element_by_class_name('lst_recentgame')
            dates = lst_recentgame.find_element_by_tag_name('th').text
            date = re.split('일', dates)[0]
            date = date.replace(" ", "")
            date = re.sub("년|월|일", ".", date)

            tbody = lst_recentgame.find_element_by_tag_name('tbody')

            inner_table = tbody.find_elements_by_tag_name('td')[2]
            sex = inner_table.find_elements_by_tag_name('th')[0].text
            sex = re.sub("자부", "", sex)

            tbody = inner_table.find_element_by_tag_name('tbody')
            trs = tbody.find_elements_by_tag_name('tr')
            homeName = trs[0].find_elements_by_tag_name('td')[0].text
            homeScore = trs[0].find_elements_by_tag_name('td')[6].text

            visitName = trs[1].find_elements_by_tag_name('td')[0].text
            visitScore = trs[1].find_elements_by_tag_name('td')[6].text

            playTime = trs[2].find_elements_by_tag_name('td')[6].text
            if len(playTime) == 5:
                playTime = re.sub("h|m", "", playTime)
                playTime = int(playTime[-2:]) + int(int(playTime[0]) * 60)
            else:
                playTime = re.sub("m", "", playTime)

            tfoot = lst_recentgame.find_element_by_tag_name('tfoot')
            stageText = tfoot.find_elements_by_tag_name('td')[1].text

            stageName = re.split('\/', stageText)[0].replace(" ", "")
            volume = re.split('\/', stageText)[2]
            volume = re.sub("관중수 |,|명", "", volume)

            self.dict['date'].append(date)
            self.dict['sex'].append(sex)
            self.dict['visitTeam'].append(visitName)
            self.dict['homeTeam'].append(homeName)
            self.dict['playTimes'].append(playTime)
            self.dict['stageName'].append(stageName)
            self.dict['volume'].append(volume)
            self.dict['visitScore'].append(visitScore)
            self.dict['homeScore'].append(homeScore)

            driverDetail.close()
            print('-------완료')

        progressBar.setValue(len(addressList))
        self.df = pd.DataFrame(self.dict)
        print("끝")

    def getSession(self, url):
        self.session_name = {'session': [], 'name': []}
        self.driver.get(url)
        time.sleep(1)

        self.driver.find_element_by_class_name('selectBox-label').click()
        a = self.driver.find_elements_by_class_name('selectBox-dropdown-menu')[0]
        lis = a.find_elements_by_tag_name('li')
        for li in lis:
            self.session_name['session'].append(li.find_element_by_tag_name('a').get_attribute('rel'))
            self.session_name['name'].append(li.find_element_by_tag_name('a').text)
        # print(self.session_name)
        self.driver.close()

    def getRange(self, session):
        url = "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=" + session
        self.driver = webdriver.Chrome("C:/Users/Administrator/PycharmProjects/PracticeDesinApi/chromedriver.exe",
                                       options=self.option)
        self.driver.get(url)
        self.driver.find_elements_by_class_name('selectBox-label')[1].click()
        self.year_month = []
        a = self.driver.find_elements_by_class_name('selectBox-dropdown-menu')[1]
        lis = a.find_elements_by_tag_name('li')
        for li in lis:
            self.year_month.append(li.find_element_by_tag_name('a').get_attribute('rel'))

        # print(self.year_month)

        # url = "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season="+session+"&team=&yymm=2016-10"
        # self.driver.get(url)


if __name__ == "__main__":
    urls = ["https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=013&team=&yymm=2016-10",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=013&team=&yymm=2016-11",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=013&team=&yymm=2016-12",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=013&team=&yymm=2017-01",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=013&team=&yymm=2017-02",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=013&team=&yymm=2017-03",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=014&team=&yymm=2017-10",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=014&team=&yymm=2017-11",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=014&team=&yymm=2017-12",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=014&team=&yymm=2018-01",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=014&team=&yymm=2018-02",
            "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=014&team=&yymm=2018-03"]

    volley = VolleyBall()
    volley.getSession(urls[0])
    volley.getRange('013')

##    dict = {'date':[],'sex': [] ,'visitTeam':[],'homeTeam':[],'playTimes': [] ,'stageName':[],'volume': [] ,'visitScore':[],'homeScore':[]}
##    dfs = pd.DataFrame(dict)
##    dfs.to_csv('volleyBall.csv', mode='w', index=False, encoding="euc-kr")
##
##    for url in urls :
##        volley.getData(url)
##        dfs = pd.concat([dfs,volley.df])
##        print(dfs)
##
##        dfs.to_csv('volleyBall.csv', mode='a', header=False, index=False, encoding="euc-kr")


