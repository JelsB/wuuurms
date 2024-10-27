from decimal import Decimal
from enum import StrEnum
from re import I
from unittest.mock import Base
import uuid
from pydantic import UUID4, BaseModel, Field, PositiveInt


class BoardGameKind(StrEnum):
    WIN = 'win'
    COOP = 'coop'
    ONE_TO_MANY = 'one-to-many'
    TEAMS = 'teams'


class BoardGameMechanic(StrEnum):
    DICE = 'dice'
    WORKER_PLACEMENT = 'worker placement'
    ENGINE_BUILDING = 'engine building'
    SET_COLLECTION = 'set collection'
    DECK_BUILDING = 'deck building'
    AREA_CONTROL = 'area control'
    AUCTIONING = 'auctioning'
    ABSTRACT = 'abstract'
    DEXTERITY = 'dexterity'
    DICE_ROLLING = 'dice rolling'
    COOPERATIVE = 'cooperative'
    PARTY_GAME = 'party game'
    HIDDEN_ROLES = 'hidden roles'
    NEGOTIATION = 'negotiation'
    PUSH_YOUR_LUCK = 'push your luck'
    PEN_AND_PAPER = 'pen and paper'


Name = Field(min_length=1, max_length=300, description='Name of the board game')


class BoardGameBase(BaseModel):
    name: str = Name
    description: str = Field(min_length=1, max_length=300, description='Description of the board game')
    min_players: PositiveInt = Field(description='Minimum number of players')
    max_players: PositiveInt = Field(description='Maximum number of players')
    min_playing_time: PositiveInt = Field(description='Minimum playing time in minutes')
    max_playing_time: PositiveInt = Field(description='Maximum playing time in minutes')
    min_age: PositiveInt = Field(description='Minimum age to play the board')
    average_rating: Decimal = Field(ge=0, le=10, description='Average rating of the board game on a scale from 0 to 10')
    complexity: Decimal = Field(ge=0, le=5, description='Complexity of the board game on a scale from 0 to 5')
    kind: BoardGameKind = Field(description='Kind of board game')
    mechanics: list[BoardGameMechanic] = Field(description='Mechanics of the board game')


class BoardGameInput(BoardGameBase):
    pass


class BoardGameOutput(BaseModel):
    name: str = Name
    id: UUID4 = Field(description='Unique identifier of the board game')


class BoardGameInDdb(BoardGameBase):
    pk: str = Field(default_factory=lambda: str(uuid.uuid4()))


class GetBoardGameOutput(BoardGameBase):
    pass
