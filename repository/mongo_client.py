from dataclasses import dataclass
import pymongo
from decouple import config



@dataclass
class DBConfig:
    host: str
    port: int
    username: str
    password: str
    database_name: str


class DocumentDBException(Exception):
    def __init__(self, message: str):
        Exception.__init__(self, message)


class DocDBConnection:
    """
    Document DB Connection
    """

    def __init__(self, config: DBConfig):
        self.host = config.host
        self.port = config.port
        self.username = config.username
        self.password = config.password
        self.database_name = config.database_name
        self.connected = False
        self._client = None

    @property
    def client(self) -> pymongo.MongoClient:
        return self._client

    def connect(self):
        """Connects to DocumentDB database

        Raises:
            DocumentDBException: connection error
        """

        try:
            self._client = pymongo.MongoClient(host=self.host,
                                               port=self.port,
                                               username=self.username,
                                               password=self.password,
                                               retryWrites=False)

            self.db = self.client.get_database(self.database_name)
            self.connected = True
        except Exception as e:
            raise DocumentDBException(f'Error trying to connect to DocumentDB database='
                                      f'{self.database_name}: {e}') from e

    def close(self):
        """Close Document DB connection

        Raises:
            DocumentDBException: connection error
        """

        try:
            if self.connected:
                self.client.close()
                self.connected = False
        except Exception as e:
            raise DocumentDBException(f'Error trying to close connection with DocumentDB database='
                                      f'{self.database_name}: {e}') from e


class DocumentDBClient:
    def __init__(self, connection: DocDBConnection, collection_name: str,
                 max_pagination_size: int = None):

        self.max_pagination_size = max_pagination_size or 1
        self.connection = connection

        if not self.connection.connected:
            self.connection.connect()

        self.collection_name = collection_name
        self.collection = self.connection.db.get_collection(collection_name)

    def insert(self, item: dict) -> str:
        """Insert a new item in a DocumentDB collection

        Args:
            item (dict): item to insert

        Raises:
            DocumentDBException: insert error

        Returns:
            dict: inserted id
        """

        try:
            result = self.collection.insert_one(item)

            return result.inserted_id
        except Exception as e:
            raise DocumentDBException(f'Error inserting record in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e

    def update(self, query_filter: dict, item: dict) -> str:
        """Update a new item in a DocumentDB collection

        Args:
            query_filter (dict): query filter
            item (dict): item to be updated

        Raises:
            DocumentDBException: update error

        Returns:
            str: upserted id
        """

        try:
            result = self.collection.update_one(query_filter, item)

            if result.matched_count == 0:
                raise DocumentDBException('No record found')
            if result.modified_count == 0:
                raise DocumentDBException('No record modified')
            if result.modified_count > 1:
                raise DocumentDBException('More than one record modified')

            return result.upserted_id
        except Exception as e:
            raise DocumentDBException(f'Error updating record in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e

    def update_all(self, filter, setup):

        try:
            result = self.collection.update_many(filter, setup)
            print('deu bom')
        except Exception as e:
            raise DocumentDBException(f'Error updating record in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e
    def find_with_pagination(self, page, limit=None, query=None, order_by=None):
        if order_by:
            sort = [(f"{order_by.get('field')}", order_by.get('order'))]
        offset = page * (self.max_pagination_size if not limit else limit)

        limit = self.max_pagination_size if not limit else limit

        if not query:
            query = {}
        try:
            content = self.collection.find(query).sort(sort).skip(offset).limit(limit)
            count_content = self.collection.count_documents(query)
            data = [x for x in content]

            return count_content, data if data else {}

        except Exception as e:
            raise DocumentDBException(f'Error finding records in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e

    def find_all(self, query, param_sort=None):
        try:
            if param_sort:
                sort = [(f"{param_sort.get('field')}", param_sort.get('order'))]
                content = self.collection.find(query).sort(sort)
            else:
                content = self.collection.find(query)
            return [x for x in content]

        except Exception as e:
            raise DocumentDBException(f'Error finding records in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e
    def find_one_or_none(self, query):
        try:
            if (self.collection.count_documents(query)) > 1:
                raise Exception('Existem mais de um resultado para essa busca')
            return self.collection.find_one(query)


        except Exception as e:
            raise DocumentDBException(f'Error finding records in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e

    def count_occurrences(self, query):
        try:
            return self.collection.count_documents(query)

        except Exception as e:
            raise DocumentDBException(f'Error finding records in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e

    def update_one(self, query, new_values):
        try:
            self.collection.update_one(query, {"$set": new_values})
        except Exception as e:
            raise DocumentDBException(f'Error finding records in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e

    def aggregate_groups(self, query):
        try:
            cursor = self.collection.aggregate(query)
            data = [x for x in cursor]

            if len(data) == 1:
                return data[0]
            if len(data) > 1:
                return data
            return {}

        except Exception as e:
            raise DocumentDBException(f'Error finding records in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e

    def aggregate_with_pagination(self, page, limit=None, query=None):
        offset = page * (self.max_pagination_size if not limit else limit)

        limit = limit or self.max_pagination_size

        query = query or []

        query_with_paginate = query + [
            {"$skip": offset},
            {"$limit": limit}
        ]

        cont_query = query + [{"$count": "count"}]
        try:
            cursor = self.collection.aggregate(query_with_paginate)
            data = [x for x in cursor]

            count_content = (self.collection.aggregate(cont_query).next()["count"]) if data else 0

            return count_content, data if data else {}

        except Exception as e:
            raise DocumentDBException(f'Error finding records in DocumentDB collection '
                                      f'{self.collection_name}: {e}') from e


def get_connection() -> DocDBConnection:
    cfg = DBConfig(
        host=config('MONGO_HOST'),
        port=config('MONGO_PORT', cast=int),
        username=config('MONGO_USER'),
        password=config('MONGO_PASS'),
        database_name=config('MONGO_DATABASE')
    )

    _connection = DocDBConnection(cfg)
    _connection.connect()

    print('Connection to DocumentDB estabilished...')

    return _connection
