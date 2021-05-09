from enum import Enum
import logging

import pymongo
import redis


MONGO_HOST = "db"
MONGO_PORT = "27017"  # default 27017


REDIS_HOST = "cache"
REDIS_PORT = "6379"  # default 6379


class CacheRedis(Enum):
    LISTINGS = 0
    NGRAMS = 1


class CacheConnection:

    def __init__(self):
        self._logger = logging.getLogger("redis")
        self._caches = {}
        self._connect_to_cache(cache_id=CacheRedis.LISTINGS)
        self._connect_to_cache(cache_id=CacheRedis.NGRAMS)

    def _connect_to_cache(self, cache_id):
        cache_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=cache_id)
        self._caches.update({cache_id: cache_conn})
    
    def cache_listing(self, key, val):
        if not self._cache_contains_listing(key, CacheRedis.LISTINGS):
            self._write_cache(key, val, db=CacheRedis.LISTINGS)
        else:
            self._logger.debug("Tried to cache a duplicate listing")


    def cache_ngrams(self, key, val):
        self._write_cache(key, val, db=CacheRedis.NGRAMS)
    

    def _cache_contains_listing(self, key):
        if self._read_cache(key, db=CacheRedis.LISTINGS):
            return True
        return False

    def _write_cache(self, key, val, cache_id):
        self._caches[cache_id].set(key, val)
    
    
    def _read_cache(key, cache_id):
        self._caches[cache_id].get(key)
    

class DatabaseConnection:
    def __init__(self):
        self._logger = logging.getLogger("redis")
        self._caches = {}
        self._connect_to_cache(cache_id=CacheRedis.LISTINGS)
        self._connect_to_cache(cache_id=CacheRedis.NGRAMS)
        
        def mongo_init():
            mongo_client = pymongo.MongoClient("mongodb://{0}:{1}".format(MONGO_HOST,
                                                                  MONGO_PORT))
    
