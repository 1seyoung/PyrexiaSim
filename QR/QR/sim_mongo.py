from pymongo import MongoClient
import time

class sim_mongo():
    def __init__(self) -> None:
        pass
    
    def data_insert(id, starting_time): # 데이터 추가 고유번호, 일 시작한 시간 : test시 time.time() 사용했음
        client = MongoClient("mongodb://localhost:27017/")
        
        db = client['sim_database'] # 데이터베이스에 접속
        
        data = {
            '_id' : id,
            'starting_time' : starting_time
        }
        
        try:
            db.personal_code.insert_one(data)
            print('data inserted!! : {} '.format(data))
            
        except:
            # 이미 고유 번호의 db존재시
            print('id {} is already exist!!'.format(id))
            
    def data_change(change_array): # 수정할 id, time이 담긴 2차원 어레이
        client = MongoClient("mongodb://localhost:27017/")
        
        db = client['sim_database'] # 데이터베이스에 접속
        
        for i in range(len(change_array)):
            id = change_array[i][0]
            change_time = change_array[i][1]
            try:
                db.personal_code.update_one({'_id' : id}, {"$set":{"starting_time" : change_time}})
                print('id : {} data changed to {}'.format(id, change_time))
            except:
                print('error!!! Check array')
            
    def data_search(id_array): # id가 담긴 어레이
        client = MongoClient("mongodb://localhost:27017/")
        result = []
        
        db = client['sim_database'] # 데이터베이스에 접속
        for i in range(len(id_array)):
            id = id_array[i]
            #private_id = db.personal_code.find_one({'_id' : id})['_id']
            starting_time = db.personal_code.find_one({'_id' : id})['starting_time']
            working_time = time.time() - starting_time
            arr = [id, working_time]
            result.append(arr)
            #print('_id = {}\nworker : {}\nworking time : {}'.format(private_id,id, working_time))
        return result