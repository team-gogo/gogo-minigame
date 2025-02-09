from sqlmodel import create_engine, SQLModel

from config import DB_HOST, DB_NAME, DB_USER, DB_PASS


DB = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

engine = create_engine(DB, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)