from copy import deepcopy
from typing import Any, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

# TODO: is this needed?
BaseModelT = TypeVar('BaseModelT', bound=BaseModel)


# It is not and will not be possible to create Optional Pydantic Models based on another model
# because of the current type implementation of Python
# see: https://github.com/pydantic/pydantic/issues/3120
def optional(model: Type[BaseModelT]) -> Type[BaseModelT]:
    """
    Creates a new Pydantic Model with all fields optional

    Args:
        model: The Pydantic Model to make all fields optional from

    Example:
    ```python
    from pydantic import BaseModel

    class User(BaseModel):
        first_name: str
        last_name: str

    @optional
    class OptionalUser(User):
        pass
    """

    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        # if not isinstance(field.default, PydanticUndefinedType):
        #     new.default = field.default
        # else:
        new.default = default

        new.annotation = Optional[field.annotation]  # pyright: ignore[reportAttributeAccessIssue]
        return (new.annotation, new)

    return create_model(
        model.__name__,
        __base__=model,
        __module__=model.__module__,
        **{field_name: make_field_optional(field_info) for field_name, field_info in model.model_fields.items()},  # pyright: ignore
    )
