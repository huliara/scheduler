from sqlalchemy.orm import Session


class SQLAlchemyBaseRepository():
    def __init__(self, db:Session):
        self.db = db
        
