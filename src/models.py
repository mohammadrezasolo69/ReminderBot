from typing import Optional,List
from datetime import datetime
from sqlalchemy import String,CheckConstraint,UniqueConstraint,DateTime,Text,ForeignKey,text
from sqlalchemy.orm import Mapped,mapped_column,relationship

from .config import BaseModel,create_table


class UserAccount(BaseModel):
    __tablename__ = 'user_accounts'

    telegram_id : Mapped[int] = mapped_column(primary_key=True,unique=True)
    phone_number : Mapped[Optional[str]] = mapped_column(String(15),unique=True,nullable=True)
    username : Mapped[Optional[str]] = mapped_column(String(50),nullable=True,unique=True)
    full_name : Mapped[Optional[str]] = mapped_column(String(50),nullable=True)
    is_active :Mapped[bool] = mapped_column(default=True)
    is_admin : Mapped[bool] = mapped_column(default=False)
    join_date : Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True)
    notes : Mapped[List['Note']] = relationship(backref="users")

    __table_args__ = (
        UniqueConstraint('telegram_id','phone_number','username',name='unique_fields_constraint'),
    )

    def __repr__(self):
        return str(self.telegram_id)


class Note(BaseModel):
    __tablename__ = 'notes'

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    content : Mapped[str] = mapped_column(Text)
    is_done :Mapped[bool] = mapped_column(default=False)
    date : Mapped[datetime] = mapped_column(DateTime)
    user_id : Mapped[int] = mapped_column(ForeignKey('user_accounts.telegram_id',ondelete='CASCADE'))

    __table_args__ = (
        CheckConstraint(text("date > CURRENT_TIMESTAMP"), name='positive_date_constraint'),
    )

    def __repr__(self):
        return self.phone_number

create_table()