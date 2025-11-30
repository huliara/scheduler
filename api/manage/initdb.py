from database import engine
from models.models import Base


def initdb():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    initdb()
