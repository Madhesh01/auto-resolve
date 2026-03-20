from redis import asyncio as aioredis
from redis.asyncio.client import Redis
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise ValueError("REDIS_URL not set in .env")

redis_client = aioredis.from_url(REDIS_URL)

