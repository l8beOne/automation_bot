from aiogram.fsm.storage.redis import DefaultKeyBuilder, Redis, RedisStorage
import config

redis = Redis(host=config.REDDIS_HOST, port=config.REDDIS_PORT, decode_responses=True)
storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_bot_id=True))