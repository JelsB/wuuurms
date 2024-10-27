import uuid
from api_old.data_access.ddb_client import DdbClient
from api_old.models.team import TeamInDdb, TeamInput, TeamOutput
from api_old.settings import table_name


def create_new_team(team: TeamInput):
    ddb_client = DdbClient(table_name().team)
    team_db = TeamInDdb(sk=team.edition, name=team.name)
    ddb_client.put_item(team_db.model_dump())
    team_out = TeamOutput(edition=team.edition, name=team.name, id=uuid.UUID(team_db.pk))

    return team_out
