from typing import Protocol, TypedDict
from aws_cdk import Stack
from aws_cdk.aws_dynamodb import Attribute, AttributeType, Billing, Capacity, ITableV2, TableV2
from constructs import Construct


class Tables(TypedDict):
    board_game_table: ITableV2


class DatabasesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        board_game_table = self.create_board_game_table()
        self.tables: Tables = {'board_game_table': board_game_table}

    def create_board_game_table(self):
        return TableV2(
            self,
            'BoardGame',
            table_name='board-game',
            billing=Billing.provisioned(
                read_capacity=Capacity.fixed(1), write_capacity=Capacity.autoscaled(max_capacity=1)
            ),
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
        )
