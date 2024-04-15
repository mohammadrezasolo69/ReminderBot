from datetime import datetime

from .models import UserAccount,Note
from .config import session




def get_user(telegram_id:int):
    exist_user = session.query(UserAccount).get(telegram_id)
    return exist_user

def all_users():
    return session.query(UserAccount).all()


def create_user(user):
    exist_user = get_user(telegram_id=user.id)
    if exist_user is not None:
        return exist_user
    
    new_user = UserAccount(
        telegram_id = user.id,
        username = user.username if user.username is not None else '',
        full_name = user.first_name if user.first_name is not None else '',
        join_date = datetime.now()
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user