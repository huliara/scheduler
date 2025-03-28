from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)

SessionLocal = UnifiedAlchemyMagicMock()

class Base(DeclarativeBase):
    pass

Base.query = SessionLocal.query_property()


# Dependency Injection用
def get_mock_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
