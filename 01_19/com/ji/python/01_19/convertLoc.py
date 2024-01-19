from cx_Oracle import connect

# Table 데이터 > 번호값 제외한 모든 데이터 > CSV 파일에 담기

arr = []
def getDataBase():
    
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
        arr.append([f"{place},{phone},{i[2]},{i[1]}"])
        
    con.close()
    
def getCSV():
    
    with open("C:\\Users\\sdedu\\Desktop\\Dev\\prac\\place.csv",'w',encoding='UTF-8') as f:
        for i in arr:
            f.write(f"{i[0]}\n")
            print(f"{i[0]} 생성 완료")

getDataBase()
getCSV()