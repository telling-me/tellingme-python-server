from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.configs import settings

_async_engine = create_async_engine(
    settings.database_url,
    pool_recycle=3600,
    echo=False,
)
_AsyncSessionFactory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=_async_engine,
)


def get_async_session_with_alchemy() -> AsyncSession:
    return _AsyncSessionFactory()
