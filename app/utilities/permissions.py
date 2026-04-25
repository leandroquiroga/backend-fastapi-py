import services
from fastapi import HTTPException, status, Depends
from utilities import logging
def require_rol(allowed_roles: list[str]):

    """Decorator para verificar el rol del usuario"""
    def dependency(current_user=Depends(services.get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return dependency
  