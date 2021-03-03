from pymongo import MongoClient
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
client = MongoClient('localhost', 27017)
db = client.LogBook

def insertTestData():
  print("db에게 보내는 중")
  db.logbook.insert_one({
        "email" : "skatjr30@naver.com",
        "num" : 2,
        "text" : "test입니다.test입니다.test입니다.test입니다.test입니다.",
        "src" :"null",
        "comment" : "멋쟁이"
  })
  print("db에게 끝")


if __name__ == '__main__':
    insertTestData()
      