from datetime import date, datetime

from discordwebhook import Discord
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.models import Shift

Discord_URL = "https://discordapp.com/api/webhooks/1087558350109163520/jly9YybhouXEbu3NB5H5Juwf336SO_1N8kcwmbqVWitlmaG4ETswsaJk0-c5uzgHBLKp"

discord = Discord(url=Discord_URL)


def alert_shortage(slot: Shift):
    message_content = f"参加者が足りていません.{slot.start_time.month}月{slot.start_time.day}日{slot.name}"
    discord.post(content=message_content)
    return


def alert_exp_shortage(slot: Shift):
    message_content = f"経験者が足りていません.{slot.start_time.month}月{slot.start_time.day}日{slot.name}"
    discord.post(content=message_content)
    return


def today_slots(db: Session):
    today=date.today()
    today_start=datetime(today.year,today.month,today.day,0,0,0)
    today_end=datetime(today.year,today.month,today.day,23,59,59)
    slots = db.scalars(
        select(Shift).filter(Shift.start_time>today_start,Shift.start_time<today_end)
    ).all()
    if slots is None:
        return
    slot_message_list=["本日のお仕事",]
    for slot in slots:
        assignees=[f'{assignee.name}' for assignee in slot.workers ]
        assignees_string=" ".join(assignees)
        slot_message_list.append(f'{slot.start_time.hour}時{slot.start_time.minute}分{slot.name}:{assignees_string}')
    message_content='\n'.join(slot_message_list)
    discord.post(content=message_content)
    return