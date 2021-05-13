from enum import Enum
import logging

import pymongo
import redis
import rq


MONGO_HOST = "db"
MONGO_PORT = "27017"  # default 27017


REDIS_HOST = "cache"
REDIS_PORT = "6379"  # default 6379


class Caches(Enum):
    LISTINGS = 0
    PARSE_JOB = 1
    NGRAMS = 2

def enqueue_parse_job(job_fn, job_input):
    queue = rq.Queue(connection=redis.Redis(host=REDIS_HOST,
                                            port=REDIS_PORT,
                                            db=Caches.PARSE_JOB))
    result = queue.enqueue(job_fn, job_input)
    

    
class GenericCache:

    def __init__(self, cache_id):
        self._logger = logging.getLogger("redis")
        self._cache_id = cache_id


    def write_cache(self, key, val):
        cache = redis.Redis(host=REDIS_HOST,
                            port=REDIS_PORT,
                            db=self._cache_id)
        return cache.set(key,val)


    def read_cache(self, key):
        cache = redis.Redis(host=REDIS_HOST,
                            port=REDIS_PORT,
                            db=self._cache_id)
        return cache.get(key)
    
class ListingCache(GenericCache):

    def __init__(self):
        super().__init__(cache_id=Caches.LISTINGS.value)
    
    def cache_listing(self, key):
        if not self._cache_contains_listing(key):
            return self.write_cache(key, 1)
        self._logger.debug("Tried to cache a duplicate listing")
        return None

    def _cache_contains_listing(self, key):
        if self.read_cache(key):
            return True
        return False


class NGramCache(GenericCache):
    
    def __init__(self):
        super().__init__(cache_id=Caches.NGRAMS.value)
        
    def cache_ngrams(self, key, val):
        return self.write_cache(key, val)

class DatabaseConnection:
    def __init__(self):
        self._logger = logging.getLogger("redis")
        self._caches = {}
        self._connect_to_cache(cache_id=Caches.LISTINGS)
        self._connect_to_cache(cache_id=Caches.NGRAMS)
        
        def mongo_init():
            mongo_client = pymongo.MongoClient("mongodb://{0}:{1}".format(MONGO_HOST,
                                                                  MONGO_PORT))
    
