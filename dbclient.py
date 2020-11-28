from os import getenv
import pymongo as pm


class DbClient:
    pass


class MongoDbClient(DbClient):
    def __init__(self, db_name, collection_name):
        self.mongo_client = pm.MongoClient(getenv('DATA_BASE'))
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data: dict):
        self.collection.insert_one(data)
