from typing import TypedDict
from aws_cdk import Stack
from aws_cdk.aws_dynamodb import Attribute, AttributeType, BillingMode, ITable, Table
from constructs import Construct


class Tables(TypedDict):
    board_game_table: ITable
    player_table: ITable
    team_table: ITable
    user_table: ITable


class DatabasesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        board_game_table = self.create_board_game_table()
        player_table = self.create_player_table()
        team_table = self.create_team_table()
        user_table = self.create_user_table()
        self.tables: Tables = {
            'board_game_table': board_game_table,
            'player_table': player_table,
            'team_table': team_table,
            'user_table': user_table,
        }

    # Not using TableV2 because it required autoscaling of write capacity
    # autoscaling creates CW alarms which cost money.
    # Switch to on-demand after we reach more than 25 RCU or 25 WCU (=free tier)

    def create_board_game_table(self):
        table = Table(
            self,
            'BoardGame2',
            table_name='board-game',
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            billing_mode=BillingMode.PROVISIONED,
            read_capacity=1,
            write_capacity=1,
        )
        table.add_global_secondary_index(
            index_name='GSI1',
            partition_key=Attribute(name='GSI1PK', type=AttributeType.STRING),
            sort_key=Attribute(name='GSI1SK', type=AttributeType.STRING),
            read_capacity=1,
            write_capacity=1,
        )

        return table

    def create_player_table(self):
        return Table(
            self,
            'Player2',
            table_name='player',
            billing_mode=BillingMode.PROVISIONED,
            read_capacity=1,
            write_capacity=1,
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            sort_key=Attribute(name='sk', type=AttributeType.STRING),
        )

    def create_team_table(self):
        return Table(
            self,
            'Team2',
            table_name='team',
            billing_mode=BillingMode.PROVISIONED,
            read_capacity=1,
            write_capacity=1,
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            sort_key=Attribute(name='sk', type=AttributeType.STRING),
        )

    def create_user_table(self):
        return Table(
            self,
            'User2',
            table_name='user',
            billing_mode=BillingMode.PROVISIONED,
            read_capacity=1,
            write_capacity=1,
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
        )
