from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import GroupId
from ddd.domain.member import IMemberRepository, MemberEntity
from ddd.domain.user import IUserRepository, UserEntity


class GroupGetAllMemberUseCase(TransactionUseCaseBase):
    def __init__(self,  member_repository:IMemberRepository,user_repository:IUserRepository):
        self.member_repository = member_repository
        self.user_repository = user_repository

    def execute(self,group_id:GroupId,room_number:str|None) -> list[UserEntity]:
        return self._transaction(group_id,room_number)

    def _transaction(self,group_id:GroupId,room_number:str|None) -> list[UserEntity]:
        member=self.member_repository.find_by_group(group_id)
        return member