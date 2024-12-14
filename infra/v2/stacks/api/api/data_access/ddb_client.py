from logging import log
from typing import Any, List, NotRequired, Optional, TypedDict, cast

from boto3 import resource
from boto3.dynamodb.conditions import Attr, AttributeExists
from botocore.exceptions import BotoCoreError
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_dynamodb.type_defs import ScanInputTableScanTypeDef

from api.observability import logger
from api.exceptions import DatabaseException, ItemNotFound


class ScanResult(TypedDict):
    """
    The result of a DynamoDB scan operation.
    """

    # TableAttributeValueTypeDef makes it harder for type checking.
    # e.g. we know that PKs cannot be all types of TableAttributeValueTypeDef
    # but we would have to introduce more type checks otherwise when using PKs
    items: List[dict[str, Any]]
    """
    The items returned by the scan.
    """

    # NOTE: maybe it would
    last_evaluated_key: NotRequired[dict[str, Any]]
    """
    The primary key of the item where the operation stopped, inclusive of the previous result set. 
    """


class DdbClient:
    def __init__(self, ddb_table_name: str):
        self.ddb_table_name = ddb_table_name
        # TODO can be replaced with a cached client create method
        # instead of creating the client in the constructor
        self._ddb_client, self._ddb_table_client = self._create_ddb_table_client()

    def _create_ddb_table_client(self) -> tuple[DynamoDBServiceResource, Table]:
        try:
            ddb_resource_client = cast(DynamoDBServiceResource, resource('dynamodb'))
            return ddb_resource_client, ddb_resource_client.Table(self.ddb_table_name)
        # TODO: catch specific exceptions
        except Exception as e:
            logger.error(f'Failed to connect to DynamoDB table: {self.ddb_table_name}. Error: {e}')
            raise DatabaseException(f'Failed to connect to DynamoDB table: {self.ddb_table_name}') from e

    def scan_table(self, limit: int, last_evaluated_key: Optional[dict] = None) -> ScanResult:
        try:
            scan_kwargs: ScanInputTableScanTypeDef = {'Limit': limit}
            if last_evaluated_key:
                scan_kwargs['ExclusiveStartKey'] = last_evaluated_key

            response = self._ddb_table_client.scan(**scan_kwargs)

            result: ScanResult = {'items': response['Items']}
            # Note: Docs just say "if empty" but don't define what empty means.
            # I presume None or empty dict, but maybe KeyError can occur. => use get() method?
            # => Empty means the key does not exist in the response.
            if last_evaluated_key_response := response.get('LastEvaluatedKey'):
                result['last_evaluated_key'] = last_evaluated_key_response
            return result

        except self._ddb_client.meta.client.exceptions.ClientError as e:
            logger.error(f'Failed to scan table {self.ddb_table_name}. Error: {e}')
            raise DatabaseException(f'Failed to scan table {self.ddb_table_name}.') from e
        except BotoCoreError as e:
            logger.error(f'Failed to scan table {self.ddb_table_name}. Error: {e}')
            raise DatabaseException(f'Failed to scan table {self.ddb_table_name}.') from e

    def get_item_from_pk(self, pk: dict[str, str]) -> dict:
        try:
            response = self._ddb_table_client.get_item(Key=pk)
            if 'Item' not in response:
                logger.error(f'Item with {pk=} not found.')
                raise ItemNotFound(item_key=pk, table=self.ddb_table_name)
            return response['Item']
        except self._ddb_client.meta.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.error(f'Table or index does not exist: {self.ddb_table_name}')
                raise DatabaseException('Table or index does not exist.') from e
            else:
                logger.error(f'Failed to get item with {pk=}. Error: {e}')
                raise DatabaseException(f'Failed to get item with {pk=}.') from e
        except BotoCoreError as e:
            logger.error(f'Failed to get item with {pk=}. Error: {e}')
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

    # def get_items_from_gsi(self, **kwargs: Unpack[QueryInputTableQueryTypeDef]) -> List[dict]:
    #     try:
    #         table: Table = self._ddb_table_client
    #         response = table.query(**kwargs)

    #         return response['Items']

    #     except table.meta.client.exceptions.ClientError as e:
    #         if e.response['Error']['Code'] == 'ResourceNotFoundException':
    #             raise DatabaseException(f'Items with GSI {gsi_name} and values {gsi_keys} not found') from e
    #         else:
    #             raise DatabaseException(f'Failed to get items with GSI {gsi_name} and values {gsi_keys}') from e
    #     except BotoCoreError as e:
    #         raise DatabaseException(f'Failed to get items with GSI {gsi_name} and values {gsi_keys}') from e

    def update_item(self, pk: dict, attributes: dict[str, Any]):
        """Updates the attributes of an item in the table.

        Args:
            pk (dict): partition key of the item
            attributes (dict[str, Any]): Dictionary of attributes to update.
              The key is the attribute name and the value is the new value.

        Raises:
            DatabaseException: Some issue with the database operation.
        """
        # Check if all the primary keys exist.
        # This supports composite primary keys (sort keys) out of the box
        pks_exist: Optional[AttributeExists] = None
        for pk_name in pk.keys():
            if not pks_exist:
                pks_exist = Attr(pk_name).exists()
            else:
                # TODO: will need to be validated with tables that use a composite key
                pks_exist = pks_exist and Attr(pk_name).exists()
        # typeguard
        assert pks_exist is not None

        try:
            # TODO: condition to check if it also exists? API call will silently be successful even if it doesn't exist.
            self._ddb_table_client.update_item(
                Key=pk,
                # Adds one or more attributes and values to an item.
                # If any of these attributes already exist, they are replaced by the new values.
                UpdateExpression='SET ' + ', '.join([f'#{key} = :val_{key}' for key in attributes.keys()]),
                ExpressionAttributeNames={f'#{key}': key for key in attributes.keys()},
                ExpressionAttributeValues={f':val_{key}': value for key, value in attributes.items()},
                ConditionExpression=pks_exist,
            )
        except self._ddb_client.meta.client.exceptions.ConditionalCheckFailedException as e:
            logger.error(
                f'Item with {pk=} in table {self.ddb_table_name} not found when trying to update with {attributes=}.'
            )
            raise ItemNotFound(pk, self.ddb_table_name) from e
        except self._ddb_client.meta.client.exceptions.ClientError as e:
            logger.error(f'Failed to update item with {pk=}. Error: {e}')
            raise DatabaseException(f'Failed to update item with {pk=} and {attributes=}.') from e
        except BotoCoreError as e:
            logger.error(f'Failed 2 to update item with {pk=}. Error: {e}')
            raise DatabaseException(f'Failed to update item with {pk=} and {attributes=}.') from e

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

    def delete_item(self, pk: dict):
        """Deletes an item from the table.

        Args:
            pk (dict): partition key of the item

        Raises:
            DatabaseException: Some issue with the database operation.
        """
        try:
            # TODO: condition to check if it also exists? API call will be successful even if it doesn't exist.
            self._ddb_table_client.delete_item(Key=pk)
        except self._ddb_client.meta.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise DatabaseException(f'Item with {pk=} not found.') from e
            else:
                raise DatabaseException(f'Failed to delete item with {pk=}.') from e
        except BotoCoreError as e:
            raise DatabaseException(f'Failed to delete item with {pk=}.') from e
