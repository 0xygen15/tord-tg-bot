import asyncio
from redis.asyncio.client import Redis

from backend.database import Database
from data.config import DB_REDIS_HOST, DB_REDIS_PORT, REDIS_PASSWORD, REDIS_USER, REDIS_USER_PASSWORD
from handlers import info, tord_game, nie_game, tof_game, themes_game

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from loader import bot


redis_instance = Redis(host=DB_REDIS_HOST, port=DB_REDIS_PORT) #create redis instance
storage = RedisStorage(redis_instance) #create storage with redis instance
dp = Dispatcher(storage=storage) #create dispatcher instance
dp.include_routers(info.router, tord_game.router, nie_game.router, tof_game.router, themes_game.router)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    Database.create_database_if_not_exists()
    Database.create_users_table()
    asyncio.run(main())
