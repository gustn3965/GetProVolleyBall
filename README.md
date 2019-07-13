# 개요
한국 프로 배구(남/녀) 데이터를 GUI를 이용하여 csv파일로 저장하기. 

python - selenium 과 PyQt5 사용함.

https://www.kovo.co.kr/game/v-league/11110_schedule_list.asp?season=014&team=&s_part=1&yymm=2017-11

해당 사이트를 들어가면, 리그별로 월별 경기가 나온다.

![homepage](./image/homepage.PNG)


해당 날짜의 상세결과를 통하여, 

![detail](./image/detail.PNG)

상세정보들을 확인할 수 있다.
저는 년도-월-일, 원정팀, 홈팀, 경기장명, 관중수, 원정팀점수, 홈팀점수 를 갖고왔습니다.

![dataColumn](./image/dataColumn.PNG)

해당 정보들을 csv파일로 저장합니다.



# 사용방법 
