# 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
import pandas as pd

# http://www.menupan.com/restaurant/bestrest/bestrest.asp?pt=rt&areacode=ss204
# 전체 내용 데이터 파싱하기
# parser 종류 : html.parser > htmt5lib 사용할 것
url = "http://www.menupan.com/restaurant/bestrest/bestrest.asp?pt=rt&areacode=ss204"
response = requests.get(url)

html = response.text
soup = BeautifulSoup(html,'html5lib')

# 해당 페이지의 순위, 상호, 업종, 주소, url에 대한 내용을 출력
# select 관련 > 하나의 열에 여러 선택자가 필요한 경우, .000 or .XXX (or : ',')

# 위의 데이터들을 list로 나타내는 작업
# ex) [{'순위':1,'상호':'XXX','업종':'한식',...},{...},{...}]
# url에 대한 내용은 따로 별개의 list로 제작.

ul = soup.select_one('body > div > div.container > div.bestRest > div.ranking > div.rankingList > ul')

# 순위
rank = ul.select('li > div > p.numTop,p.rankNum')

# 상호
name = ul.select('li > p.listName > span > a')

# 업종
category = ul.select('li > p.listType')

# 주소
locale = ul.select('li > p.listArea')

# 정보를 넣어줄 빈 리스트들 생성
allList = []
allUrl = []

for i in range(0,0+25):

    # url 속성 가져오기
    urls = ul.select('li > p.listName > span > a')[i]['href']

    # 딕셔너리 생성 후, 리스트에 넣어줌.
    arr = {'순위':rank[i].text,'상호': name[i].text,'업종':category[i].text,'주소':locale[i].text}
    allList.append(arr)

    # URL 용 리스트 따로 생성
    allUrl.append(urls)

# 출력
print('-'*30)
for i in allList:
    urls = allUrl[int(i['순위'])-1]
    print(f"순위 : {i['순위']}")
    print(f"상호 : {i['상호']}")
    print(f"업종 : {i['업종']}")
    print(f"주소 : {i['주소']}")
    print(f'url : {urls}')
    print('-'*30)
  
  
# menuList를 가지고 순위를 index로 하는 DataFrame을 생성

idxArr = []

# data.set_index('순위',inplace=True) 를 사용하면 보다 간편하게 인덱스로 생성해 줄 수 있음!
# 현재 사용한 방법은 리스트에 순위만 빼내서, 그 리스트를 다시 데이터 프레임 생성하면서 넣어주었음.

for i in range(0,25):
    idxArr.append(allList[i]['순위'])

print(idxArr)

for i in range(0,25):
    df = pd.DataFrame(allList,idxArr)

df

# 기본 주소값 뒤에 별도로 담아놓은 주소값 붙여서
# 전화번호, 상세주소를 가져오기
basicUrl = 'https://www.menupan.com'

allAddr = []

for i in range(0,25):

    # 위에서 크롤링했던 과정과 같지만, 각각의 Url이 다르기 때문에, for 문을 사용하여 각각 다른 Url에서 긁어온 값을 리스트에 딕셔너리로 추가해준다.
    # 이렇게 리스트에 딕셔너리로 추가하는 이유는, pandas를 사용해 dataFrame으로 만들기 위함.
    dl = "http://www.menupan.com"+allUrl[i]
    response2 = requests.get(dl)
    html2 = response2.text
    soup = BeautifulSoup(html2,'html5lib')

    ul = soup.select_one('body > center > div.WrapMain > div.mainArea01 > div.areaBasic')
    tel = ul.select_one('dl.restTel > dd')

    # 주소가 두 개
    addr1 = ul.select_one('dl.restAdd > dd.add1')

    # 안양 > 서울로 바꾸면서 새주소가 없는 경우가 있어서, 삭제
    # addr2 = ul.select_one('dl.restAdd > dd.add2')

    # Separator로 / 를 주었음.
    addSum = addr1.getText() # + " / " + addr2.getText()
    allAddr.append({'전화 번호':tel,'상세 주소':addSum})
  
print(allAddr)

# dataFrame 생성, 이전에 있던 index Array를 사용하여 생성하였음.
df2 = pd.DataFrame(allAddr,idxArr)
df2

# 만들어놓은 DataFrame에 붙이기(+ '주소' 열은 삭제)
# index가 같기 때문에, 자동으로 inner Join함.

resDf = pd.concat([df, df2], axis=1)

# 주소 열 삭제
resDf = resDf.drop('주소',axis=1)
resDf

# 업종이 한식인 가게의 정보만 출력
resDf[resDf['업종']=='한식']

# 특정 구에 있는 가게의 정보만 출력
# Series Split : resDf['상세 주소'].str.split().str[2] 이런식으로 사용해서, 특정 Series 지정 > 나눔 > 나눈 것에서 특정 인자 지정
# Fancy Index를 통해 나누어놓은 구가 원하는 것 일 경우의 DataFrame을 출력한다. 

# str.contains('') 로도 찾을 수 있음.
resDf[resDf['상세 주소'].str.split().str[1]=='강서구']


