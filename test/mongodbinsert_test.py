from pymongo import MongoClient
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
client = MongoClient('localhost', 27017)
db = client.LogBook

def insertTestData():
  print("db에게 보내는 중")
  todolist = list(db.logbook.find({'email':'keumks789@naver.com','num':1},{'_id':False}))
  print(todolist)
  print("db에게 끝")


if __name__ == '__main__':
    insertTestData()
      