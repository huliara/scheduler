from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import GroupId
from ddd.domain.member import IMemberRepository, MemberEntity
from ddd.domain.user import UserId


class GroupActivateMemberUseCase(TransactionUseCaseBase):
    def __init__(self, member_repository:IMemberRepository):
        self.member_repository=member_repository
        
    def execute(self,group_id:GroupId,user_id:UserId):
        return self._transaction(group_id,user_id)
    
    def _transaction(self,group_id:GroupId,user_id:UserId)->MemberEntity:
        try:
            member=self.member_repository.find_by_id(group_id,user_id)
        except:
            raise UseCaseException(f'group_id:{group_id} not found')
        member.is_active=True
        new_group=self.member_repository.save(member)
        return new_group