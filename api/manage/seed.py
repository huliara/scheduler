import os
import sys
import datetime

# プロジェクトルートディレクトリをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.dirname(current_dir)
sys.path.append(api_dir)

from database import SessionLocal
from ddd.infra.repository.user_repository import UserRepository
from ddd.infra.repository.group_repository import GroupRepository
from ddd.infra.repository.member_repository import MemberRepository
from ddd.infra.repository.task_repository import TaskRepository
from ddd.infra.repository.template_repository import TemplateRepository

from ddd.domain.user.user_entity import UserEntity
from ddd.domain.group.group_entity import GroupEntity
from ddd.domain.member.member_entity import MemberEntity
from ddd.domain.task.task_entity import TaskEntity
from ddd.domain.template.template_entity import TemplateEntity
from ddd.domain.template.template_value_object import TemplateSlot
from manage.initdb import initdb

def seed():
    session = SessionLocal()
    initdb()  # データベースを初期化
    
    # Repositories
    user_repo = UserRepository(session)
    group_repo = GroupRepository(session)
    member_repo = MemberRepository(session)
    task_repo = TaskRepository(session)
    template_repo = TemplateRepository(session)

    try:
        # User creation
        print("Creating Users...")
        admin_entity = UserEntity(
            id=None,
            name="tsunekawa",
            room_number="B312",
            exp_tasks=[],
            is_admin=True,
            is_active=True
        )
        admin = user_repo.add(admin_entity, "password")
        
        group_entity = GroupEntity(
            id=None,
            name="B3",
            members=[],
            tasks=[],
            template=[]
        )
        group = group_repo.add(group_entity)

        # Task creation
        print("Creating Tasks...")
        jimuto_entity = TaskEntity(
            id=None,
            name="事務当番",
            group_id=group.id,
            max_worker=2,
            min_worker=1,
            exp_worker=1,
            wage=2300,
            duration=datetime.timedelta(hours=2),
            permissions=[],
            creater_id=admin.id,
            subtask=[]
        )
        task1 = task_repo.add(jimuto_entity)

        tomari_jimuto_entity = TaskEntity(
            id=None,
            name="泊まり事務当番",
            group_id=group.id,
            max_worker=2,
            min_worker=1,
            exp_worker=1,
            wage=5000,
            duration=datetime.timedelta(hours=10),
            permissions=[],
            creater_id=admin.id,
            subtask=[]
        )
        task2 = task_repo.add(tomari_jimuto_entity)
        task3_entity = TaskEntity(
            id=None,
            name="朝皿洗い",
            group_id=group.id,
            max_worker=4,
            min_worker=3,
            exp_worker=2,
            wage=2000,
            duration=datetime.timedelta(hours=1),
            permissions=[],
            creater_id=admin.id,
            subtask=[]
        )
        task3 = task_repo.add(task3_entity)
        task4_entity = TaskEntity(
            id=None,
            name="朝食販売",
            group_id=group.id,
            max_worker=2,
            min_worker=1,
            exp_worker=1,
            wage=2100,
            duration=datetime.timedelta(hours=1,minutes=45),
            permissions=[],
            creater_id=admin.id,
            subtask=[]
        )
        task4 = task_repo.add(task4_entity)
        task5_entity = TaskEntity(
            id=None,
            name="昼皿洗い",
            group_id=group.id,
            max_worker=4,
            min_worker=3,
            exp_worker=2,
            wage=2000,
            duration=datetime.timedelta(hours=1),
            permissions=[],
            creater_id=admin.id,
            subtask=[]
        )
        task5 = task_repo.add(task5_entity)
        task6_entity = TaskEntity(
            id=None,
            name="昼食販売",
            group_id=group.id,
            max_worker=2,
            min_worker=1,
            exp_worker=1,
            wage=2700,
            duration=datetime.timedelta(hours=2,minutes=15),
            permissions=[],
            creater_id=admin.id,
            subtask=[]
        )
        task6 = task_repo.add(task6_entity)

        task7_entity = TaskEntity(
            id=None,
            name="夕食販売",
            group_id=group.id,
            max_worker=2,
            min_worker=1,
            exp_worker=1,       
            wage=2400,
            duration=datetime.timedelta(hours=2),
            permissions=[],
            creater_id=admin.id,
            subtask=[]
        )
        task7 = task_repo.add(task7_entity)
        
        users = []
        for i in range(1, 6):
            user_entity = UserEntity(
                id=None,
                name=f"user{i}",
                room_number=f"B30{i}",
                exp_tasks=[] if i == 0 else [task1.id,task2.id,task3.id,task4.id,task5.id,task6.id,task7.id],
                is_admin=False,
                is_active=True
            )
            created_user = user_repo.add(user_entity, "password")
            users.append(created_user)
        
        # Member creation (GroupUser)
        print("Adding members to Group...")
        all_users = [admin] + users
        for user in all_users:
            member_entity = MemberEntity(
                user_id=user.id,
                group_id=group.id,
                name=user.name,
                is_active=True,
                point=0,
                exp_tasks=[]
            )
            member_repo.add(member_entity)
            
        
        
        
        # Template creation
        print("Creating Template...")
        # Note: TemplateSlot expects task_id, date_from_start, start_time, task_name
        jimuto_slots=[]
        for i in range(7):
            jimuto_slots.append(TemplateSlot(
                task_id=task1.id,
                date_from_start=i,
                start_time=datetime.time(20, 0),
                task_name=task1.name
            ))
            jimuto_slots.append(TemplateSlot(
                task_id=task2.id,
                date_from_start=i,
                start_time=datetime.time(22, 0),
                task_name=task2.name
            ))
            for j in range(6):
                jimuto_slots.append(TemplateSlot(
                    task_id=task1.id,
                    date_from_start=i+1,
                    start_time=datetime.time(8+j*2, 0),
                    task_name=task1.name
                ))

        template_entity = TemplateEntity(
            id=None,
            name="平日シフト",
            group_id=group.id,
            slots=set(jimuto_slots)
        )
        template_repo.add(template_entity)
        
        suijito_slots=[]
        for i in range(7):
            suijito_slots.append(TemplateSlot(
                task_id=task3.id,
                date_from_start=i,
                start_time=datetime.time(7, 0),
                task_name=task3.name
            ))
            suijito_slots.append(TemplateSlot(
                task_id=task4.id,
                date_from_start=i,
                start_time=datetime.time(8, 0),
                task_name=task4.name
            ))
            suijito_slots.append(TemplateSlot(
                task_id=task5.id,
                date_from_start=i,
                start_time=datetime.time(11, 0),
                task_name=task5.name
            ))
            suijito_slots.append(TemplateSlot(
                task_id=task6.id,
                date_from_start=i,
                start_time=datetime.time(12, 0),
                task_name=task6.name
            ))
            suijito_slots.append(TemplateSlot(
                task_id=task7.id,
                date_from_start=i,
                start_time=datetime.time(17, 0),
                task_name=task7.name
            ))
        
        template_entity2 = TemplateEntity(
            id=None,
            name="炊事当番シフト",
            group_id=group.id,
            slots=set(suijito_slots)
        )
        template_repo.add(template_entity2)
    except Exception as e:
        session.rollback()
        print(f"Error creating seed data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    seed()
