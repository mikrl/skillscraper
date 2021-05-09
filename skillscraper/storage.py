from enum import Enum
import logging

import pymongo
import redis


MONGO_HOST = "db"
MONGO_PORT = "27017"  # default 27017


REDIS_HOST = "cache"
REDIS_PORT = "6379"  # default 6379


class Caches(Enum):
    LISTINGS = 0
    NGRAMS = 1


class CacheConnection:

    def __init__(self):
        self._logger = logging.getLogger("redis")
        self._caches = {}
        self._connect_to_cache(cache_id=Caches.LISTINGS)
        self._connect_to_cache(cache_id=Caches.NGRAMS)

    def _connect_to_cache(self, db):
        cache_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=db)
        self._caches.update({db: cache_conn})
    
    def cache_listing(self, key):
        if not self._cache_contains_listing(key):
            return self._write_cache(key, 1, db=Caches.LISTINGS)
        self._logger.debug("Tried to cache a duplicate listing")
        return None


    def cache_ngrams(self, key, val):
        return self._write_cache(key, val, db=Caches.NGRAMS)    

    def _cache_contains_listing(self, key):
        if self._read_cache(key, db=Caches.LISTINGS):
            return True
        return False

    def _write_cache(self, key, val, db):
        return self._caches[db].set(key, val)
    
    
    def _read_cache(self, key, db):
        self._caches[db].get(key)
    

class DatabaseConnection:
    def __init__(self):
        self._logger = logging.getLogger("redis")
        self._caches = {}
        self._connect_to_cache(cache_id=Caches.LISTINGS)
        self._connect_to_cache(cache_id=Caches.NGRAMS)
        
        def mongo_init():
            mongo_client = pymongo.MongoClient("mongodb://{0}:{1}".format(MONGO_HOST,
                                                                  MONGO_PORT))
    
