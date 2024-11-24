from decimal import Decimal
from enum import StrEnum
from typing import Literal, Optional
import uuid
from pydantic import UUID4, BaseModel, Field, PositiveInt, model_validator

from api.utils.models import optional


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
ID = Field(description='Unique identifier of the board game')


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
    state: Literal['active', 'inactive'] = Field(
        'active', description='State of the board game. Inactive means it is not available during the event.'
    )


@optional
class BoardGameOptionalBase(BoardGameBase):
    pass


class BoardGameInput(BoardGameBase):
    pass


class BoardGameOutput(BaseModel):
    name: str = Name
    id: UUID4 = ID


class BoardGameInDdb(BoardGameBase):
    pk: str = Field(default_factory=lambda: str(uuid.uuid4()))
    GSI1PK: str
    GSI1SK: str


class BoardGameOptionalInDdb(BoardGameOptionalBase):
    GSI1PK: Optional[str]
    GSI1SK: Optional[str]


class ListFilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100, description='Number of items to return')
    # Don't use skip but implement pagination with the last item from the previous page
    # This is more efficient when the number of items is large
    start_id: UUID4 | None = Field(None, description='The board game id to start listing from')
    # The user also needs to provide the name of the board game to start listing from because ExclusiveStartKey needs all PK and GSI1SK values
    # NOTE: it could be more user friendly to just ask for the id and then do an extra DDB fetch in the backend. But this is slower.
    start_name: str | None = Field(
        None, min_length=1, max_length=300, description='The board game name to start listing from'
    )
    order_by_name: Literal['alphabetically', 'reverse alphabetically'] = Field(
        'alphabetically',
        description='How to order the board games based on their name. Descending means alphabetically and',
    )

    @model_validator(mode='after')
    def check_start_id_and_start_name(cls, values):
        start_id = values.start_id
        start_name = values.start_name
        if (start_id and not start_name) or (start_name and not start_id):
            raise ValueError('If start_id is provided, start_name must also be provided. And vice versa.')
        return values


class GetBoardGameOutput(BoardGameBase):
    id: UUID4 = ID


class UpdateBoardGameInput(BoardGameOptionalBase):
    pass


class OptionalBoardGameInDdb(BoardGameBase):
    pass
