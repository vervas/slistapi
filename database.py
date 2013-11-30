from pymongo import MongoClient

class MongoConnection():
    def __init__(self, host='localhost', port=27017, db='', collection=''):
        client = MongoClient(host, port)
        self.db = client[db][collection]
