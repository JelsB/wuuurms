import uuid
from pydantic import UUID4, BaseModel, Field


class BoardGameBase(BaseModel):
    name: str
    description: str


class BoardGameInput(BoardGameBase):
    pass


class BoardGameOutput(BoardGameBase):
    pass


class BoardGameInDdb(BoardGameBase):
    pk: UUID4 = Field(default_factory=lambda: uuid.uuid4().hex)
