from abc import ABC
from enum import Enum
import logging
import pickle

import pymongo
import redis
import rq

from aggregator import map_ngrams, reduce_ngrams

MONGO_HOST = "db"
MONGO_PORT = "27017"  # default 27017


REDIS_HOST = "cache"
REDIS_PORT = "6379"  # default 6379


class Caches(Enum):
    LISTINGS = 0
    PARSE_JOB = 1
    NGRAMS = 2


class JobQueue:
    def enqueue_parse_job(job_fn, job_input):
        queue = rq.Queue(connection=redis.Redis(host=REDIS_HOST,
                                                port=REDIS_PORT,
                                                db=Caches.PARSE_JOB))
        result = queue.enqueue(job_fn, job_input)
    

    
class GenericCache(ABC):

    def __init__(self, cache_id):
        self._logger = logging.getLogger("redis")
        self._cache_id = cache_id

    @abstractmethod
    def _process_update(self, old_val, new_val):
        pass

    def write_cache(self, key, val):
        cache = redis.Redis(host=REDIS_HOST,
                            port=REDIS_PORT,
                            db=self._cache_id)
        pickled_val = pickle.dumps(val)
        return cache.set(key, pickled_val)


    def read_cache(self, key):
        cache = redis.Redis(host=REDIS_HOST,
                            port=REDIS_PORT,
                            db=self._cache_id)

        pickled_val = cache.get(key)
        val = pickle.loads(pickled_val)
        return val

    def update_cache(self, key, val):
        existing_val = self.read_cache(key)
        new_val = self._process_update(existing_val, val)
        return self.write_cache(key, new_val)

    
    def contains(self, key):
        if self.read_cache(key):
            return True
        return False
    
class ListingCache(GenericCache):

    def __init__(self):
        super().__init__(cache_id=Caches.LISTINGS.value)
    
    def cache_listing(self, key):
        if not self.contains(key):
            return self.write_cache(key, 1)
        self._logger.debug("Tried to cache a duplicate listing")
        return None

    def _process_update(self, old_val, new_val):
        return new_val


class NGramCache(GenericCache):
    
    def __init__(self):
        super().__init__(cache_id=Caches.NGRAMS.value)
        
    def cache_ngrams(self, key, val):
        if self.contains(key):
            return self.update_
        return self.write_cache(key, val)

    def update_ngrams(self, key, val):
        existing_ngrams = self.read_cache(key)
        new_val = reduce_ngrams([existing_ngrams, val])
        return self.write_cache(key, new_val)

    def _process_update(self, old_val, new_val):
        return reduce_ngrams(old_val, new_val)

        
class DatabaseConnection:
    def __init__(self):
        self._logger = logging.getLogger("redis")
        self._caches = {}
        self._connect_to_cache(cache_id=Caches.LISTINGS)
        self._connect_to_cache(cache_id=Caches.NGRAMS)
        
        def mongo_init():
            mongo_client = pymongo.MongoClient("mongodb://{0}:{1}".format(MONGO_HOST,
                                                                  MONGO_PORT))
    



