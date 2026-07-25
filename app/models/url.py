from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Url(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    original_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    short_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    clicks: Mapped[int] = mapped_column(
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )