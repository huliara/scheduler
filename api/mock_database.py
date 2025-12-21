from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy import create_engine
from models.models import Base

engine = create_engine('sqlite:///:memory:', echo=True)

SessionLocal = UnifiedAlchemyMagicMock()

Base.metadata.create_all(engine)
