from pydantic import BaseModel, ConfigDict, Field


class BoxUserListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="主键ID")
    avatar: str | None = Field(default=None, description="头像")
    nickname: str | None = Field(default=None, description="用户昵称")
    account: str | None = Field(default=None, description="用户账号")
    mobile: str | None = Field(default=None, description="用户电话")
    login_time: int | None = Field(default=None, description="最后登录时间（时间戳/整型）")


class BoxUserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="主键ID")
    avatar: str | None = Field(default=None, description="头像")
    nickname: str | None = Field(default=None, description="用户昵称")
    mobile: str | None = Field(default=None, description="用户电话")
    sex: int | None = Field(default=None, description="用户性别")
    user_money: float | None = Field(default=None, description="用户余额")


class BoxUserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    avatar: str | None = None
    nickname: str | None = None
    account: str | None = None
    mobile: str | None = None
    login_time: int | None = None


class BoxUserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    avatar: str | None = None
    nickname: str | None = None
    account: str | None = None
    mobile: str | None = None
    login_time: int | None = None
