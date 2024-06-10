from functools import wraps
from fastapi import HTTPException

def handle_route_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"an unexpected error occurred in {func.__name__}: {e}")
    return wrapper
