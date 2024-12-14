from api.data_access.ddb_client import DdbClient
from api.entities.user.models import GetUserOutput, UserInDdb, CreateUserInput, CreateUserOutput
from api.settings import table_name


def create_new_user(user: CreateUserInput):
    ddb_client = DdbClient(table_name().user)
    user_db = UserInDdb(**user.model_dump(), pk=user.username)
    ddb_client.put_item(user_db.model_dump())
    user_out = CreateUserOutput(username=user.username)

    return user_out


def get_user(username: str):
    ddb_client = DdbClient(table_name().user)
    user_from_db = ddb_client.get_item_from_pk({'pk': username})
    user_out = GetUserOutput(**user_from_db, username=user_from_db['pk'])
    return user_out


def get_users(limit: int, start_username: str = None):
    ddb_client = DdbClient(table_name().user)
    last_evaluated_key = {'pk': start_username} if start_username else None
    users_from_db = ddb_client.scan_table(limit, last_evaluated_key)

    users_out = [GetUserOutput(**user, username=user['pk']) for user in users_from_db['items']]
    return users_out
