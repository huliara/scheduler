from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.member import IMemberRepository, MemberEntity


class GroupGetAllMemberUseCase(TransactionUseCaseBase):
    def __init__(self, db, member_repository:IMemberRepository,):
        super().__init__(db)
        self.member_repository = member_repository

    def execute(self,group_id:GroupId,room_number:str|None) -> list[MemberEntity]:
        return self._transaction(group_id,room_number)

    def _transaction(self,group_id:GroupId,room_number:str|None) -> list[MemberEntity]:
        result = self.member_repository.find_all(group_id,room_number)
        return result