from typing import TypedDict
from aws_cdk import Stack
from aws_cdk.aws_dynamodb import (
    Attribute,
    AttributeType,
    Billing,
    Capacity,
    GlobalSecondaryIndexPropsV2,
    ITableV2,
    TableV2,
)
from constructs import Construct


class Tables(TypedDict):
    board_game_table: ITableV2
    player_table: ITableV2
    team_table: ITableV2
    user_table: ITableV2


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

    def create_board_game_table(self):
        return TableV2(
            self,
            'BoardGame',
            table_name='board-game',
            billing=Billing.provisioned(
                read_capacity=Capacity.fixed(1), write_capacity=Capacity.autoscaled(max_capacity=1)
            ),
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            global_secondary_indexes=[
                GlobalSecondaryIndexPropsV2(
                    index_name='GSI1',
                    partition_key=Attribute(name='GSI1PK', type=AttributeType.STRING),
                    sort_key=Attribute(name='GSI1SK', type=AttributeType.STRING),
                )
            ],
        )

    def create_player_table(self):
        return TableV2(
            self,
            'Player',
            table_name='player',
            billing=Billing.provisioned(
                read_capacity=Capacity.fixed(1), write_capacity=Capacity.autoscaled(max_capacity=1)
            ),
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            sort_key=Attribute(name='sk', type=AttributeType.STRING),
        )

    def create_team_table(self):
        return TableV2(
            self,
            'Team',
            table_name='team',
            billing=Billing.provisioned(
                read_capacity=Capacity.fixed(1), write_capacity=Capacity.autoscaled(max_capacity=1)
            ),
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            sort_key=Attribute(name='sk', type=AttributeType.STRING),
        )

    def create_user_table(self):
        return TableV2(
            self,
            'User',
            table_name='user',
            billing=Billing.provisioned(
                read_capacity=Capacity.fixed(1), write_capacity=Capacity.autoscaled(max_capacity=1)
            ),
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
        )
