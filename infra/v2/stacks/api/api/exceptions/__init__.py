class ConfigurationException(Exception):
    def __init__(self, message='Configuration Error') -> None:
        super().__init__(message)


class InternalServiceException(Exception):
    def __init__(self, message='Internal Service Error'):
        super().__init__(message)


class DatabaseException(Exception):
    def __init__(self, message='Database Service Error') -> None:
        super().__init__(message)
