from api.data_access.ddb_client import DdbClient
from api.entities.user.models import GetUserOutput, GetUsersOutput, UserInDdb, CreateUserInput, CreateUserOutput
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


def get_users(limit: int, start_username: str = None) -> GetUsersOutput:
    ddb_client = DdbClient(table_name().user)
    last_evaluated_key = {'pk': start_username} if start_username else None
    users_from_db = ddb_client.scan_table(limit, last_evaluated_key)

    users_out = [GetUserOutput(**user, username=user['pk']) for user in users_from_db['items']]

    # explicit check because it's NotRequired and this is the most type safe way to do so.
    # NOTE: maybe it would be easier to have it required and return None if it's not there.
    # because the output model requires it
    optional_args = {}
    if 'last_evaluated_key' in users_from_db:
        optional_args['last_evaluated_username'] = users_from_db['last_evaluated_key']['pk']
    # Do not pass default values explicitly because otherwise they will be included in the response
    # even when response_model_exclude_unset = True is set
    return GetUsersOutput(users=users_out, **optional_args)
