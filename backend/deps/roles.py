# deps/roles.py
from fastapi import Depends, HTTPException, status
from dependencies import get_current_user_payload

def role_required(allowed_roles: list[str]):
    def wrapper(current_user_payload: dict = Depends(get_current_user_payload)):
        user_role = current_user_payload.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied for role: {user_role}"
            )
        return current_user_payload
    return wrapper
