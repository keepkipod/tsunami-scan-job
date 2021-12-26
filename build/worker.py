#!/usr/bin/env python3

import rediswq
import subprocess


host = "redis-master"
QUEUE = "scan-queue"
# Uncomment next two lines if you do not have Kube-DNS working.
# import os
# host = os.getenv("REDIS_SERVICE_HOST")

q = rediswq.RedisWQ(name=QUEUE, host=host)
print("Worker with sessionID: " +  q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))
while not q.empty():
  item = q.lease(lease_secs=10, block=True, timeout=2)
  if item is not None:
    itemstr = item.decode("utf-8")
    print("Working on " + itemstr)
    subprocess.call(["./entrypoint.sh", itemstr])
    q.complete(item)
  else:
    print("Waiting for work")
print("Queue empty, exiting")
