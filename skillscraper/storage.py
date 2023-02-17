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
        queue = rq.Queue(
            connection=redis.Redis(
                host=REDIS_HOST, port=REDIS_PORT, db=Caches.PARSE_JOB
            )
        )
        result = queue.enqueue(job_fn, job_input)


class DatabaseConnection:
    def __init__(self):
        self._logger = logging.getLogger("redis")
        self._caches = {}
        self._connect_to_cache(cache_id=Caches.LISTINGS)
        self._connect_to_cache(cache_id=Caches.NGRAMS)

        def mongo_init():
            mongo_client = pymongo.MongoClient(
                "mongodb://{0}:{1}".format(MONGO_HOST, MONGO_PORT)
            )
