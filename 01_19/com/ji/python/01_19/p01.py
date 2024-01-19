from http.client import HTTPSConnection
from urllib.parse import quote
from json import loads
from cx_Oracle import connect
from numpy import place


# eb43c48551b94f0ddc100b8a8020d311

# https://dapi.kakao.com${FORMAT}

# 위도 / 경도
# 37.563992 / 126.8119787

# 검색어를 콘솔에 입력 > 위도 / 경도 지정 > 반경 1km 이내에 있는 > 검색어에 대한 위치 정보를 알아낼 것.

# 장소명(업체이름), 전화번호, 경도, 위도

# DB에 저장
# 전화번호가 없는 업체가 있기 떄문에, 없는 업체는 '-'로 대체해 줌.
# 경도, 위도 : 소수점 6자릿수까지만 받아올 것.

# NVL 함수 : null 일 때 지정한 값으로 대치하는 함수
# NVL(value,(값이) null 일 때 대체할 값)
# SELECT NVL(null,'-'),NVL('NULL','-') FROM dual
# 'NULL'을 주면 문자열이기 때문에 대치가 안됨!

# NVL2 함수 : null의 여부에 따라서 지정한 값으로 대치하는 함수
# NVL2(value,값이 있을때 대체값,값이 없을 때 대체값)
# SELECT NVL2(null,'A','B'),NVL2('NULL','A','B') FROM dual

types = 'GET'
url = 'dapi.kakao.com'
query = '/v2/local/search/keyword.json?y=37.563992&x=126.8119787&radius=1000&query='
headers = {'Authorization': 'KakaoAK eb43c48551b94f0ddc100b8a8020d311'}
arr = []

# Kakao REST API Parsing / .json
def getMySearch():
    
    print()
    print()
    searchM = quote(input('검색할 정보를 입력해주세요 : '))
    q = query+searchM
    
    hc = HTTPSConnection(url)
    hc.request(types,q,headers=headers)
    
    res = hc.getresponse()
    resBody = res.read().decode('utf-8')
    
    checkData = loads(resBody)   
    place,phone,x,y = '','','',''

    # get place_name, phone, x, y
    for i in range(0,len(checkData['documents'])): 
        
        place = checkData['documents'][i]['place_name']
        if (checkData['documents'][i]['phone'] == '') or (checkData['documents'][i]['phone'] == ' '):      
            phone = '-'
        else:
            phone = checkData['documents'][i]['phone']
        x = f"{float(checkData['documents'][i]['x']):.6f}"
        y = f"{float(checkData['documents'][i]['y']):.6}"
        
        arr.append({'업체명':place,'전화번호':phone,'x':x,'y':y})
    
        print(f"업체명 : {place}\n전화번호 : {phone}\n위도 : {y}\n경도 : {x}")
        print('-'*40)
        
    print()
        
        
# Insert DataBase
def insertDataBase():
    
    con = connect('respina/sdj7524@localhost:1521/xe')
    
    for i in range(0,len(arr)):
        
        info = arr[i]['업체명'] + '/' + arr[i]['전화번호']
        sql  = f"INSERT INTO place VALUES(\'{info}\',{arr[i]['x']},{arr[i]['y']})"
        cur = con.cursor() 
        
        try:
            cur.execute(sql)
            
            if cur.rowcount == 1:
                print(f"{info} 등록 성공!")
                con.commit()
            else:
                print(f"{info} 등록 실패!")
                
        except Exception:
            print(f"{arr[i]['업체명']} 는(은) 이미 등록된 업체입니다!")
            
    print()
    con.close()
    
# Select DataBase
def selectDataBase():
    
    con = connect('respina/sdj7524@localhost:1521/xe')
    sql = 'SELECT * FROM place'

    cur = con.cursor()
    cur.execute(sql)

    for i in cur:
        
        info = i[0].split('/',1)
        place = info[0]
        phone = info[1]
        print(f"업체명 : {place}\n전화번호 : {phone}\n위도 : {i[2]}\n경도 : {i[1]}")
        print('-'*40)
        
    print()

while True:
    print('-'*40)
    print('1. 지역 정보 받아오기')
    print('2. 받아온 지역 정보 DB에 입력')
    print('3. DB 정보 확인')
    print('4. 나가기')
    
    try:
        print('-'*40)
        num = int(input('메뉴 입력 : '))
        print()
        
        if num not in [1,2,3,4]:
            print('메뉴 내의 숫자를 입력해주세요!')
            
        elif num == 1:
            arr.clear()
            print('-'*40)
            getMySearch()
            
        elif num == 2:
            if not arr:
                print('먼저 지역 정보를 받아와주세요!')
                
            else:
                print('-'*40)
                insertDataBase()
                
        elif num == 3:
            print('-'*40)
            selectDataBase()
            
        else:
            break
        
    except Exception:
        print('정수만 입력해주세요!')
    