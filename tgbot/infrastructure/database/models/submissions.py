from datetime import datetime
import enum
from typing import Optional

from sqlalchemy import String, Boolean, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, TableNameMixin


class EducationLevel(enum.Enum):
    SCHOOL = 'school'
    COLLEGE = 'college'
    BACHELOR = 'bachelor'
    MASTERS = 'masters'


class Submission(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_user_id: Mapped[int] = mapped_column(
        ForeignKey("tgusers.id"),
        nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    area_id: Mapped[int] = mapped_column(ForeignKey("mahallas.id"), nullable=False)
    photo: Mapped[str] = mapped_column(String(255), nullable=False)
    education: Mapped[str] = mapped_column(String(255), nullable=False)
    education_level: Mapped[Optional[EducationLevel]] = mapped_column(
        Enum(EducationLevel),
        nullable=True
    )
    profession: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    certificate: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    creative_work: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    is_accepted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    tguser = relationship("TgUser", back_populates="submissions")

    def __repr__(self):
        return f"<Submission {self.id}-{self.full_name}>"
