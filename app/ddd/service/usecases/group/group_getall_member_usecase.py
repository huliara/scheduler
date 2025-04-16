from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.member import IMemberRepository, MemberEntity
from app.ddd.domain.user import IUserRepository, UserEntity


class GroupGetAllMemberUseCase(TransactionUseCaseBase):
    def __init__(self, db, member_repository:IMemberRepository,user_repository:IUserRepository):
    
        super().__init__(db)
        self.member_repository = member_repository
        self.user_repository = user_repository

    def execute(self,group_id:GroupId,room_number:str|None) -> list[UserEntity]:
        return self._transaction(group_id,room_number)

    def _transaction(self,group_id:GroupId,room_number:str|None) -> list[UserEntity]:
        member=self.member_repository.find_by_group_id(group_id)
        return member