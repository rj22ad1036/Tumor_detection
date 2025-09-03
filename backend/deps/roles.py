# deps/roles.py
from fastapi import Depends, HTTPException, status
from dependencies import get_current_user_payload
from models import User

def role_required(allowed_roles: list[str]):
    def wrapper(current_user: User = Depends(get_current_user_payload)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied for role: {current_user.role}"
            )
        return current_user
    return wrapper
