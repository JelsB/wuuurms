from copy import deepcopy
from typing import Any, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

# TODO: is this needed?
BaseModelT = TypeVar('BaseModelT', bound=BaseModel)


def optional(model: Type[BaseModelT]) -> Type[BaseModelT]:
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
