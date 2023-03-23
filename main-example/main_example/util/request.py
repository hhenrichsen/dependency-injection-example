from typing import TypeVar, Callable

from flask import request


A = TypeVar('A')

def get_query_param_or_def(key: str, default: A, parse: Callable[[str], A] = lambda x: x) -> A:
    if key in request.args and (value := request[key]) is not None:
        return parse(value)
    else:
        return default
    
def get_body_param_or_error(errors: list[str], key: str, type):
    body = request.json
    if key not in body:
        errors.append(f"'{key}' is a required {type.__name__} (missing)")
        return None
    if (value := body[key]) is None: 
        errors.append(f"'{key}' is a required {type.__name__} (present but no value)")
        return None
    if not isinstance(value, type):    
        errors.append(f"'{key}' is a required {type.__name__} (invalid type)")
        return None
    return value