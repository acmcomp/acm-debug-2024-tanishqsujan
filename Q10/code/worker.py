import os

import redis
from rq import Worker, Queue, Connection

listen = ['task_queue']

redis_url = 'redis://:610n8i64nVyWtVFkk8dZb3RelvbU09hd@redis-11025.c322.us-east-1-2.ec2.redns.redis-cloud.com:11024'

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()