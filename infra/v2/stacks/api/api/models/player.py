from pydantic import BaseModel, Field, NonNegativeInt

UserName = Field(min_length=1, max_length=30, description='Username of the player')
Edition = Field(min_length=1, max_length=30, description='Event Edition that the Player was present')


class PlayerBase(BaseModel):
    display_name: str = Field(min_length=1, max_length=30, description='Display name of the player')


class PlayerInput(PlayerBase):
    username: str = UserName
    edition: str = Edition


class PlayerOutput(PlayerBase):
    username: str = UserName
    edition: str = Edition


class PlayerInDdb(PlayerBase):
    pk: str = UserName
    sk: str = Edition
    score: NonNegativeInt = 0
