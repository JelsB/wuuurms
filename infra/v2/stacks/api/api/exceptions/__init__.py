class ConfigurationException(Exception):
    def __init__(self, message='Configuration Error') -> None:
        super().__init__(message)


class InternalServiceException(Exception):
    def __init__(self, message='Internal Service Error'):
        super().__init__(message)


class DatabaseException(Exception):
    def __init__(self, message='Database Service Error') -> None:
        super().__init__(message)


class ItemNotFound(DatabaseException):
    def __init__(self, item_key: dict, table: str) -> None:
        message = f'Item with {item_key} not found in table {table}'
        super().__init__(message)
