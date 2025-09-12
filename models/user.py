
import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import IDMixin, TimestampsMixin


class User(Base, IDMixin, TimestampsMixin):

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    profile: Mapped['Profile'] = relationship(
        back_populates='user',
        cascade="all, delete-orphan",
        uselist=False
    )


class Profile(Base, IDMixin):
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False, unique=True)

    first_name: Mapped[str] = mapped_column(String, nullable=True)
    sur_name:  Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped['User'] = relationship(back_populates='profile')
