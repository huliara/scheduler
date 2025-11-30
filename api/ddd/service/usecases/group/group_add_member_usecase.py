from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import GroupId, IGroupRepository
from ddd.domain.member import IMemberRepository, MemberEntity
from ddd.domain.user import UserId


class GroupAddMemberUseCase(TransactionUseCaseBase):
    def __init__(self, group_repository: IGroupRepository, member_repository:IMemberRepository):
        self.group_repository = group_repository
        self.member_repository = member_repository

    def execute(self, group_id:GroupId,user_ids:list[UserId]) -> list[MemberEntity]:
        return self._transaction(group_id,user_ids)

    def _transaction(self, group_id:GroupId,user_ids:list[UserId]) -> list[MemberEntity]:
        try:
            _= self.group_repository.find_by_id(group_id)
        except:
            raise UseCaseException(f'group_id:{group_id} not found')
        target_members=[]
        for user_id in user_ids:
            member = self.member_repository.find_by_id(group_id,user_id)
            if member is not None:
                raise UseCaseException(f'member_id:{user_id} is already in group_id:{group_id}')
            member = MemberEntity(user_id=user_id,group_id=group_id)
            target_members.append(member)
        result=self.member_repository.bulk_add(group_id,target_members)
        return result