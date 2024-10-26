from pydantic import BaseModel, Field

UserName = Field(min_length=1, max_length=30, description='Username of the player')


class UserBase(BaseModel):
    pass


class UserInput(UserBase):
    username: str = UserName


class UserOutput(UserBase):
    username: str = UserName


class UserInDdb(UserBase):
    pk: str = UserName
