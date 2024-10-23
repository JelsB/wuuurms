from enum import StrEnum
import uuid
from pydantic import UUID4, BaseModel, Field


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


class BoardGameBase(BaseModel):
    name: str = Field(min_length=1, max_length=300, description='Name of the board game')
    description: str = Field(min_length=1, max_length=300, description='Description of the board game')
    min_players: int = Field(ge=1, description='Minimum number of players')
    max_players: int = Field(ge=1, description='Maximum number of players')
    min_playing_time: int = Field(ge=1, description='Minimum playing time in minutes')
    max_playing_time: int = Field(ge=1, description='Maximum playing time in minutes')
    min_age: int = Field(ge=1, description='Minimum age to play the board')
    average_rating: float = Field(ge=0, le=10, description='Average rating of the board game on a scale from 0 to 10')
    complexity: float = Field(ge=0, le=5, description='Complexity of the board game on a scale from 0 to 5')
    kind: BoardGameKind = Field(description='Kind of board game')
    mechanics: list[BoardGameMechanic] = Field(description='Mechanics of the board game')


class BoardGameInput(BoardGameBase):
    pass


class BoardGameOutput(BoardGameBase):
    pass


class BoardGameInDdb(BoardGameBase):
    pk: UUID4 = Field(default_factory=lambda: uuid.uuid4().hex)
