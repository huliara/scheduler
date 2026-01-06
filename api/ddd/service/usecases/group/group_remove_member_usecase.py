from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import GroupId, IGroupRepository
from ddd.domain.member import IMemberRepository, MemberEntity
from ddd.domain.user.user_value_object import UserId


class GroupRemoveMemberUseCase(TransactionUseCaseBase):
    def __init__(self, group_repository: IGroupRepository, member_repository:IMemberRepository):
        self.group_repository = group_repository
        self.member_repository = member_repository

    def execute(self, group_id:GroupId,user_id:UserId) -> MemberEntity:
        return self._transaction(group_id,user_id)

    def _transaction(self, group_id:GroupId,user_id:UserId) -> MemberEntity:
        try:
            _= self.group_repository.find_by_id(group_id)
        except:
            raise UseCaseException(f'group_id:{group_id} not found')
        result=self.member_repository.remove(user_id,group_id)
        return result