from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from pymongo import MongoClient

class Database:
    client: MongoClient = None

    @classmethod
    def connect(cls):
        if not cls.client:
            cls.client = MongoClient("mongodb://localhost:27017/")
        return cls.client

    @classmethod
    def get_client(cls):
        return cls.client

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()
            cls.client = None

class MongoDBMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, database_name: str, collection_name: str):
        super().__init__(app)
        self.database_name = database_name
        self.collection_name = collection_name

    async def dispatch(self, request: Request, call_next):
        request.state.db_client = Database.get_client()
        request.state.db = request.state.db_client[self.database_name]
        request.state.collection = request.state.db[self.collection_name]
        response = await call_next(request)
        return response