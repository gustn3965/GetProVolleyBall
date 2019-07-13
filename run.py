import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import os
import pandas as pd
import VolleyBall

form_class = uic.loadUiType("volley.ui")[0]


class VolleyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.getSession()
        self.row_text = {'row': [], 'text': []}

        for i in self.volley.session_name['name']:
            item = QListWidgetItem(i)
            self.listWidget.addItem(item)
        self.listWidget.show()

        self.pushButton.clicked.connect(self.btn_clicked1)
        self.dfd = QListView()
        self.df = QListWidget()

        self.setTableWidgetData()
        self.progressBar.setValue(0)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.pushButton_2.clicked.connect(self.btn_clicked_2)

        self.pushButton_3.clicked.connect(self.btn_clicked_3)

        self.pushButton_4.clicked.connect(self.btn_clicked_4)

        self.threadClass = ThreadClass()

        self.pushButton_6.clicked.connect(self.btn_clicked_6)

        self.pushButton_7.clicked.connect(self.btn_clicked_7)

        self.pushButton_5.clicked.connect(self.btn_clicked_5)

        self.pushButton_8.clicked.connect(self.btn_clicked_8)

    def getSession(self):
        self.volley = VolleyBall.VolleyBall()
        self.volley.getSession("https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=014")

    # 해당 리그 가져오기
    def btn_clicked1(self):

        self.label.setText(" 가져오는 중...")
        rows = self.listWidget_2.count()

        if rows > 0:
            self.listWidget_2.clear()

        row = self.listWidget.currentRow()
        self.league_name = self.listWidget.currentItem().text()
        session = self.volley.session_name['session'][row]
        self.volley.getRange(session)

        for i in self.volley.year_month:
            item = QListWidgetItem(i)
            self.listWidget_2.addItem(item)
        self.label.setText("완료")

    def setTableWidgetData(self):
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(9)
        data_column_header = ['date', 'sex', 'visitTeam', 'homeTeam', 'playTimes', 'stageName', 'volume', 'visitScore',
                              'homeScore']
        self.tableWidget.setHorizontalHeaderLabels(data_column_header)

    # 해당 날짜 가져오기
    def btn_clicked_2(self):
        colum_idx_lookup = {'date': 0, 'sex': 1, 'visitTeam': 2, 'homeTeam': 3, 'playTimes': 4, 'stageName': 5,
                            'volume': 6, 'visitScore': 7, 'homeScore': 8}

        row = self.listWidget.currentRow()
        session = self.volley.session_name['session'][row]
        date = self.listWidget_2.currentItem().text()

        url = "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=" + session + "&team=&yymm=" + date
        print(url)

        self.volley.getData(url, self.progressBar)

        self.tableWidget.setRowCount(len(self.volley.dict['date']))

        print(self.volley.dict)

        for k, v in self.volley.dict.items():
            col = colum_idx_lookup[k]
            for row, val in enumerate(v):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))

    # 저장하기.
    def btn_clicked_3(self):
        filter = "csv(*.csv)"

        fname = QFileDialog.getSaveFileName(self, caption='data', filter=filter)

        print(fname[0])
        self.volley.df.to_csv(fname[0], mode='a', index=False, encoding="euc-kr")
        print(len(fname))

    # 모든 날짜 가져오기
    def btn_clicked_4(self):
        self.worker = QThread()
        self.worker.start()

        items = []
        for index in range(0, self.listWidget_2.count()):
            items.append(self.listWidget_2.item(index).text())

        colum_idx_lookup = {'date': 0, 'sex': 1, 'visitTeam': 2, 'homeTeam': 3, 'playTimes': 4, 'stageName': 5,
                            'volume': 6, 'visitScore': 7, 'homeScore': 8}

        print(items)
        row = self.listWidget.currentRow()
        session = self.volley.session_name['session'][row]

        for date in items:
            url = "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=" + session + "&team=&yymm=" + date
            print(url)

            self.label.setText(date + " 가져오는 중...")
            self.volley.getData(url, self.progressBar)

            self.tableWidget.setRowCount(len(self.volley.dict['date']))

            for k, v in self.volley.dict.items():
                col = colum_idx_lookup[k]
                for row, val in enumerate(v):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))

    # -> 추가하기
    def btn_clicked_6(self):

        selectList = self.listWidget.currentItem().text()
        self.row_text['text'].append(selectList)

        self.row_text['row'].append(self.listWidget.currentRow())

        print(self.row_text)
        self.listWidget_3.addItem(QListWidgetItem(selectList))

    # <- 삭제하기
    def btn_clicked_7(self):

        selectList = self.listWidget_3.currentItem().text()
        idx = self.row_text['text'].index(selectList)
        del self.row_text['text'][idx]
        del self.row_text['row'][idx]
        self.listWidget_3.takeItem(self.listWidget_3.currentRow())

        print(self.row_text)


    # 선택한 리그 모두 csv파일로 저장하기
    def btn_clicked_5(self):

        filePath = QFileDialog.getExistingDirectory(self, '폴더를 선택해주세요')

        # session 구하고,
        sessionList = []
        rowList = self.row_text['row']
        for i in rowList:
            session = self.volley.session_name['session'][i]
            self.volley.getRange(session)

            for date in self.volley.year_month:
                url = "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=" + session + "&team=&yymm=" + date
                print(url)
                self.volley.getData(url, self.progressBar)
                self.volley.df.to_csv(str(filePath) + "/" + session + "_" + date + ".csv", mode='a', index=False,
                                      encoding="euc-kr")


    # 여러개 데이터 한개로 합치기
    def btn_clicked_8(self):
        filePath = QFileDialog.getExistingDirectory(self, '폴더를 선택해주세요')
        print(filePath)
        file_list = os.listdir(filePath)

        print(file_list)

        dict = {'date': [], 'sex': [], 'visitTeam': [], 'homeTeam': [], 'playTimes': [], 'stageName': [],
                            'volume': [], 'visitScore': [], 'homeScore': []}
        dfs = pd.DataFrame(dict)
        for file in file_list :
            print(str(filePath)+"/"+file)
            df = pd.read_csv(str(filePath)+"/"+file,encoding="euc-kr", index_col=False)
            dfs = pd.concat([dfs,df])


        print(dfs)

        dfs.to_csv(filePath+"/result.csv", encoding="euc-kr",index=False,mode='w')






class ThreadClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):

        items = []
        for index in range(0, self.listWidget_2.count()):
            items.append(self.listWidget_2.item(index).text())

        print(items)
        row = self.listWidget.currentRow()
        session = self.volley.session_name['session'][row]
        for date in items:
            url = "https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=" + session + "&team=&yymm=" + date
            print(url)

            self.label.setText(date + " 가져오는 중...")
            self.volley.getData(url, self.progressBar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = VolleyWindow()
    myWindow.show()
    app.exec_()