from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, synonym

from app.database import Base


class BoxUser(Base):
    __tablename__ = "box_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sn: Mapped[int] = mapped_column(Integer)
    account: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(32))
    is_disable: Mapped[int] = mapped_column(Integer)
    is_admin: Mapped[int | None] = mapped_column(Integer)

    avatar: Mapped[str | None] = mapped_column(String(200))
    real_name: Mapped[str | None] = mapped_column(String(32))
    nickname: Mapped[str | None] = mapped_column(String(32))
    mobile: Mapped[str | None] = mapped_column(String(32))
    sex: Mapped[int | None] = mapped_column(Integer)
    channel: Mapped[int | None] = mapped_column(Integer)
    login_ip: Mapped[str | None] = mapped_column(String(200))
    user_money: Mapped[Decimal | None] = mapped_column(Numeric(20, 6))
    login_time: Mapped[int | None] = mapped_column(Integer)
    invite: Mapped[int | None] = mapped_column(Integer)
    is_matchmaker: Mapped[int | None] = mapped_column(Integer)
    is_new_user: Mapped[int | None] = mapped_column(Integer)
    total_recharge_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 6))
    total_commission: Mapped[Decimal | None] = mapped_column(Numeric(10, 6))
    withdraw: Mapped[str | None] = mapped_column(String(255))
    create_time: Mapped[int | None] = mapped_column(Integer)
    update_time: Mapped[int | None] = mapped_column(Integer)
    delete_time: Mapped[int | None] = mapped_column(Integer)

    email = synonym("account")
    hashed_password = synonym("password")

    @property
    def is_active(self) -> bool:
        return int(self.is_disable or 0) == 0

    @property
    def is_superuser(self) -> bool:
        return int(self.is_admin or 0) == 1

    @property
    def is_verified(self) -> bool:
        return True
