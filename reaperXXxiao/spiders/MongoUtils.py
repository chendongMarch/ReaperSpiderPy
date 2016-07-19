# coding:utf-8
import pymongo


class MongoUtils:
    name = 'unname'

    def __init__(self, name):
        self.name = name

    @staticmethod
    def getDb():
        # 192.168.1.19
        # 3520f327-1cb2-4a94-9cee-9c6a9e4b8695
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['xxxiao']
        # db[''].insert()
        return db

    @staticmethod
    def getCol(db, colName):
        return db[colName]

    @staticmethod
    def insert(collection, infomation):
        collection.insert(infomation)

    @staticmethod
    def updateOrInsert(collection, infomation):
        newDict = {}
        for key in infomation.keys():
            if key != 'time_stamp':
                newDict[key] = infomation[key]
        num = collection.find(newDict).count()
        if num<=0:
            collection.insert(infomation)

    @staticmethod
    def find(collection, spec):
        collection.find(spec)

    @staticmethod
    def isExistWhole(collection, infomation):
        num = collection.find(infomation).count()
        if num > 0:
            return True
        else:
            return False

