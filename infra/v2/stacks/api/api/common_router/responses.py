from typing import Any, Dict
from fastapi import status

from api.common_router.models import HTTPExceptionModel


HTTP_RESPONSES: Dict[int, Dict[int | str, Dict[str, Any]]] = {
    status.HTTP_404_NOT_FOUND: {
        status.HTTP_404_NOT_FOUND: {'description': 'Board game not found', 'model': HTTPExceptionModel}
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'Internal server error', 'model': HTTPExceptionModel}
    },
}
