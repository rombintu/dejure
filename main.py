# from core import db
from bot import run
from core import log
import asyncio

# async def main():
#     log.info("All services are starting...")
#     await bot_run

if __name__ == "__main__":
    asyncio.run(run())