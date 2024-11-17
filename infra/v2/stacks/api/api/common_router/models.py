from pydantic import BaseModel


class HTTPExceptionModel(BaseModel):
    """Model to create openApi documentation for HTTP exceptions"""

    detail: str
