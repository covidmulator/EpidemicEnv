import time
import ray

@ray.remote
def f():
  time.sleep(.1)
  return ray.services.get_node_ip_address()

ray.init(redis_address='master:6379')

ids = set(ray.get[f.remote() for i in range(1000)])
print(ids)