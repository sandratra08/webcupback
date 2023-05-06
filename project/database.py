from tortoise import Tortoise
from core.credentials import settings


async def database():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={'models': ['project.models']}
    )
