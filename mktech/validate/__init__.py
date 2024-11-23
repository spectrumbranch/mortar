from typing import Any, Optional, Type, TypeGuard, TypeVar

from mktech.message import invalid_type

_T = TypeVar("_T")


def check_type(
    obj: Any,
    expected_type: Type[_T],
    message: Optional[str] = None
) -> TypeGuard[_T]:
    if not isinstance(obj, expected_type):
        if message is None:
            raise TypeError(invalid_type.format(obj, expected_type, type(obj)))
        else:
            raise TypeError(message)

    return True


def ensure_type(
    obj: Any,
    expected_type: Type[_T],
    message: Optional[str] = None
) -> _T:
    if not isinstance(obj, expected_type):
        if message is None:
            raise TypeError(invalid_type.format(obj, expected_type, type(obj)))
        else:
            raise TypeError(message)

    return obj
