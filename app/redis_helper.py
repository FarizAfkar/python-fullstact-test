import redis
import json
from app.config import Config

redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

def cache_client_data(slug, data):
    redis_client.set(slug, json.dumps(data), ex=3600)  # Cache for 1 hour

def get_cached_client(slug):
    data = redis_client.get(slug)
    return json.loads(data) if data else None