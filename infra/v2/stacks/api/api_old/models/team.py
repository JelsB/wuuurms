import uuid
from pydantic import UUID4, BaseModel, Field, NonNegativeInt

Edition = Field(min_length=1, max_length=30, description='Event Edition that the Player was present')


class TeamBase(BaseModel):
    name: str = Field(min_length=1, max_length=40, description='Name of the team')


class TeamInput(TeamBase):
    edition: str = Edition


class TeamOutput(TeamBase):
    edition: str = Edition
    id: UUID4 = Field(description='Unique identifier of the team')


class TeamInDdb(TeamBase):
    pk: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sk: str = Edition
    score: NonNegativeInt = 0
