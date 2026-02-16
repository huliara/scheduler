import sys
import os
# プロジェクトルートディレクトリ(apiディレクトリ)をパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.dirname(current_dir)
sys.path.append(api_dir)

from database import engine
from models.models import Base


def initdb():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    initdb()
