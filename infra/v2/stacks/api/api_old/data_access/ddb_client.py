from typing import Any, List, cast

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import BotoCoreError
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table

from api_old.observability import logger
from api_old.exceptions import DatabaseException


class DdbClient:
    def __init__(self, ddb_table_name: str):
        self.ddb_table_name = ddb_table_name
        # TODO can be replaced with a cached client create method
        # instead of creating the client in the constructor
        self._ddb_client, self._ddb_table_client = self._create_ddb_table_client()

    def _create_ddb_table_client(self) -> tuple[DynamoDBServiceResource, Table]:
        try:
            ddb_resource_client = cast(DynamoDBServiceResource, boto3.resource('dynamodb'))
            return ddb_resource_client, ddb_resource_client.Table(self.ddb_table_name)
        # TODO: catch specific exceptions
        except Exception as e:
            logger.error(f'Failed to connect to DynamoDB table: {self.ddb_table_name}. Error: {e}')
            raise DatabaseException(f'Failed to connect to DynamoDB table: {self.ddb_table_name}') from e

    def get_item_from_pk(self, pk: dict[str, str]) -> dict:
        try:
            response = self._ddb_table_client.get_item(Key=pk)
            return response['Item']  # TODO: typeguard for non-existant item key. Will this not just return Exception?
        except self._ddb_client.meta.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise DatabaseException(f'Item with {pk=} not found.') from e
            else:
                raise DatabaseException(f'Failed to get item with {pk=}.') from e
        except BotoCoreError as e:
            raise DatabaseException(f'Failed to get item with {pk=}.') from e

    def get_batch_items_from_pk(self, pks: List[dict]):
        try:
            logger.debug(f'Batch get item request: {pks} for table: {self.ddb_table_name}')
            response = self._ddb_client.batch_get_item(RequestItems={self.ddb_table_name: {'Keys': pks}})
            logger.debug(f'Batch get item response: {response}')
            items = response['Responses'][self.ddb_table_name]
            if not items:
                logger.warning(f'No items found for {pks} in table {self.ddb_table_name}')
            return items
        except self._ddb_client.meta.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise DatabaseException('An item with partition key was not found in the batch request.') from e
            else:
                raise DatabaseException('Failed to get a batch of items with partition keys.') from e
        except BotoCoreError as e:
            raise DatabaseException('Failed to get a batch of player with partition keys.') from e

    def get_items_from_gsi(self, gsi_name: str, gsi_keys: dict[str, str]) -> List[dict]:
        key_condition_expression = None
        for key, value in gsi_keys.items():
            key_condition_expression = (
                Key(key).eq(value)
                if key_condition_expression is None
                else key_condition_expression & Key(key).eq(value)
            )
        # typeguard
        assert key_condition_expression is not None

        try:
            table: Table = self._ddb_table_client
            response = table.query(IndexName=gsi_name, KeyConditionExpression=key_condition_expression)

            return response['Items']

        except table.meta.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise DatabaseException(f'Items with GSI {gsi_name} and values {gsi_keys} not found') from e
            else:
                raise DatabaseException(f'Failed to get items with GSI {gsi_name} and values {gsi_keys}') from e
        except BotoCoreError as e:
            raise DatabaseException(f'Failed to get items with GSI {gsi_name} and values {gsi_keys}') from e

    def update_item(self, pk: dict, attributes: dict[str, Any]):
        """Updates the attributes of an item in the table.

        Args:
            pk (dict): partition key of the item
            attributes (dict[str, Any]): Dictionary of attributes to update.
              The key is the attribute name and the value is the new value.

        Raises:
            DatabaseException: Some issue with the database operation.
        """
        try:
            self._ddb_table_client.update_item(
                Key=pk,
                UpdateExpression='SET ' + ', '.join([f'{key} = :{key}' for key in attributes.keys()]),
                ExpressionAttributeValues={f':{key}': value for key, value in attributes.items()},
            )
        except self._ddb_client.meta.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise DatabaseException(f'Item with {pk=} not found.') from e
            else:
                raise DatabaseException(f'Failed to update item with {pk=}.') from e
        except BotoCoreError as e:
            raise DatabaseException(f'Failed to update item with {pk=}.') from e

    def put_item(self, item: dict):
        """Puts an item into the table.

        Args:
            item (dict): Dictionary of the item to put into the table.

        Raises:
            DatabaseException: Some issue with the database operation.
        """
        try:
            self._ddb_table_client.put_item(Item=item)
        except self._ddb_client.meta.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise DatabaseException(f'Item with {item=} not found.') from e
            else:
                raise DatabaseException(f'Failed to put item with {item=}.') from e
        except BotoCoreError as e:
            raise DatabaseException(f'Failed to put item with {item=}.') from e
