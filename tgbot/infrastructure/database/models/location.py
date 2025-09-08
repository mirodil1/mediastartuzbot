from typing import Optional
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base, TimestampMixin, TableNameMixin


class Region(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Region {self.name}>"

    class Meta:
        ordering = ["name"]


class District(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Optional: Add relationship for querying
    region: Mapped["Region"] = relationship("Region", back_populates="districts")
    
    def __repr__(self):
        return f"<District {self.name}>"

    class Meta:
        ordering = ["name"]


class Mahalla(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "mahalla"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Optional: Add relationship for querying
    district: Mapped["District"] = relationship("District", back_populates="mahallas")
    
    def __repr__(self):
        return f"<Mahalla {self.name}>"

    class Meta:
        ordering = ["name"]


Region.districts = relationship("District", back_populates="region", cascade="all, delete")
District.mahallas = relationship("Mahalla", back_populates="district", cascade="all, delete")
