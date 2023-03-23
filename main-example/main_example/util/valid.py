from typing import TypeVar

A = TypeVar('A')

def validate_param(name: str, value: A, valid_type):
    if value is None:
        raise ValueError(f"'{name}' is a required value -- it cannot be None")
    if isinstance((types := valid_type), list):
        if not any(map(lambda type: isinstance(value, type), types)):    
            names = ' or '.join(map(lambda type: f"'{type.__name__}'", types))
            raise TypeError(f"'{name}' must be {names} (got {type(value).__name__})")
    else:
        if not isinstance(value, valid_type):
            raise TypeError(f"'{name}' must be a {valid_type.__name__} (got {type(value).__name__})")