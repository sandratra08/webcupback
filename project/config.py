from tortoise import Tortoise, run_async
from database import database


async def main():
    await database()
    await Tortoise.generate_schemas()

    if __name__ == '__main__':
        run_async(main())
