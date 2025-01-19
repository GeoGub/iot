from collections.abc import AsyncGenerator

from settings import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), echo=True, future=True
)

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


# async def init_db(session: AsyncSession) -> None:
#     # Tables should be created with Alembic migrations
#     # But if you don't want to use migrations, create
#     # the tables un-commenting the next lines

#     # This works because the models are already imported and registered from app.models
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

#     user = await session.exec(
#         select(UserModel).where(UserModel.email == settings.FIRST_SUPERUSER_EMAIL)
#     )
#     user = user.first()
#     if not user:
#         user = CreateUserSchema(
#             email=settings.FIRST_SUPERUSER_EMAIL,
#             password=settings.FIRST_SUPERUSER_PASSWORD,
#             username=settings.FIRST_SUPERUSER_USERNAME,
#             is_superuser=True,
#             first_name="Admin",
#             last_name="Admin",
#         )
#         user = await create_user(session=session, user_create=user)


async def get_db() -> AsyncGenerator[AsyncSession, None, None]:
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session