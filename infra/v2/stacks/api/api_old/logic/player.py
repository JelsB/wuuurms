from api_old.data_access.ddb_client import DdbClient
from api_old.models.player import PlayerInDdb, PlayerInput, PlayerOutput
from api_old.settings import table_name


def create_new_player(player: PlayerInput):
    ddb_client = DdbClient(table_name().player)
    player_db = PlayerInDdb(pk=player.username, sk=player.edition, display_name=player.display_name)
    ddb_client.put_item(player_db.model_dump())
    player_out = PlayerOutput(username=player.username, edition=player.edition, display_name=player.display_name)

    return player_out
