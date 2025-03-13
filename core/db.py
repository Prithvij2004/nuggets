from sqlmodel import create_engine, Session, SQLModel

from core.config import settings

engine = create_engine(str(settings.POSTGRES_DATABASE_URL))

async def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
