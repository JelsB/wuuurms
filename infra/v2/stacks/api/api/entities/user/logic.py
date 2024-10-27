from api.data_access.ddb_client import DdbClient
from api.entities.user.models import UserInDdb, UserInput, UserOutput
from api.settings import table_name


def create_new_user(user: UserInput):
    ddb_client = DdbClient(table_name().user)
    user_db = UserInDdb(pk=user.username)
    ddb_client.put_item(user_db.model_dump())
    user_out = UserOutput(username=user.username)

    return user_out
