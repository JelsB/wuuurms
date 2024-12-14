from pydantic import BaseModel, Field

UserName = Field(min_length=1, max_length=30, description='Username of the player')


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=120, description='First name of the user')
    last_name: str = Field(min_length=1, max_length=120, description='Last name of the user')


class CreateUserInput(UserBase):
    username: str = UserName


class CreateUserOutput(BaseModel):
    username: str = UserName


class UserInDdb(UserBase):
    # This is the unique username created by cognito
    pk: str = UserName


class GetUserOutput(UserBase):
    username: str = UserName
