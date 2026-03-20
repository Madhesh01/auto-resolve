import redis.asyncio as aioredis
from dotenv import load_dotenv
import os


load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise ValueError("REDIS_URL not set in .env")

redis_client = aioredis.from_url(REDIS_URL)

async def main():
    while True:
        res = await redis_client.blpop("ticket_queue")
        print(res[1])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())