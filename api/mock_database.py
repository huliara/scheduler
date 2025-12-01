from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine('sqlite:///:memory:', echo=True)

SessionLocal = UnifiedAlchemyMagicMock()

class Base(DeclarativeBase):
    pass


Base.metadata.create_all(engine)
