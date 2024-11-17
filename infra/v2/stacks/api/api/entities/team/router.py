from fastapi import APIRouter, status

import api.entities.team.logic as logic
from api.entities.team.models import TeamInput, TeamOutput

router = APIRouter(prefix='/teams', tags=['teams'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_team(team: TeamInput) -> TeamOutput:
    team_out = logic.create_new_team(team)
    return team_out
