from abc.collections import ABC, abstractmethod
from enum import Enum
import json
import logging
import redis

from skillscraper import REDIS_HOST, REDIS_PORT


class Subcaches(Enum):
    LISTINGS = 0
    PARSE_JOB = 1
    NGRAMS = 2


class GenericCache(ABC):
    def __init__(self, cache_id):
        self._logger = logging.getLogger("redis")
        self._cache_id = cache_id

    @abstractmethod
    def _process_update(self, old_val, new_val):
        pass

    def write_cache(self, key: str, val: str) -> bool:
        cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=self._cache_id)
        return cache.set(key, val)

    def read_cache(self, key: str) -> str:
        cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=self._cache_id)
        val = cache.get(key)
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
        super().__init__(cache_id=Subcaches.LISTINGS.value)

    def cache_listing(self, key):
        if not self.contains(key):
            return self.write_cache(key, 1)
        self._logger.debug("Tried to cache a duplicate listing")
        return None

    def _process_update(self, old_val, new_val):
        return new_val


# class NGramCache(GenericCache):
#     def __init__(self):
#         super().__init__(cache_id=Subcaches.NGRAMS.value)

#     def cache_ngrams(self, key, val):
#         if self.contains(key):
#             return self.update_
#         return self.write_cache(key, val)

#     def update_ngrams(self, key, val):
#         existing_ngrams = self.read_cache(key)
#         new_val = reduce_ngrams([existing_ngrams, val])
#         return self.write_cache(key, new_val)

#     def _process_update(self, old_val, new_val):
#         return reduce_ngrams(old_val, new_val)
