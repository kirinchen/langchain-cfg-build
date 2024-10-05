from typing import List, Optional, Dict, Type, TypeVar, get_origin, get_args
from enum import Enum
from dataclasses import dataclass

T = TypeVar('T')


def convert_by_dict(data: Dict, clazz: Type[T]) -> T:
    # Get class annotations (type hints)
    annotations = clazz.__annotations__

    # Prepare arguments for class initialization
    init_args = {}
    for key, value in data.items():
        if key in annotations:
            field_type = annotations[key]
            value = _handle_value(field_type=field_type, value=value)
            init_args[key] = value

    # Create an instance of the class
    return clazz(**init_args)


def _handle_value(field_type: any, value: any) -> any:
    origin_type = get_origin(field_type)
    if origin_type is not None:  # Handle generic types like List, Optional, etc.
        if origin_type is list:
            inner_type = get_args(field_type)[0]  # Extract the type of the list elements
            return [_handle_value(inner_type, v) for v in value]
        elif origin_type is Optional:
            inner_type = get_args(field_type)[0]  # Extract the inner type of Optional
            if value is None:
                return None
            return _handle_value(inner_type, value)

    # Handle Enum
    if isinstance(field_type, type) and issubclass(field_type, Enum):
        if isinstance(value, str):
            return field_type[value]

    # Handle nested class
    if isinstance(field_type, type) and hasattr(field_type, '__annotations__'):
        return convert_by_dict(value, field_type)

    return value


# Example classes

@dataclass
class MyA:
    id: int
    name: str
    active: bool
    description: Optional[str] = None

@dataclass
class MyClass:
    a_list: List[MyA]
    a_main: Optional[MyA] = None


if __name__ == '__main__':
    data = {
        "a_list": [
            {"id": 1, "name": "Item 1", "active": True},
            {"id": 2, "name": "Item 2", "active": False, "description": "Some description"}
        ],
        "a_main": {"id": 3, "name": "Main Item", "active": True}
    }

    my_obj = convert_by_dict(data, MyClass)
    print(my_obj)
