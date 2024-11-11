# app/api/v1/endpoints/login.py
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.core.config import get_settings
from app.api import deps
from app.schemas.token import Token
from app.models.operario import Operario

settings = get_settings()
router = APIRouter()

@router.post("/login/qr", response_model=Token)
def login_qr(
    *,
    db: Session = Depends(deps.get_db),
    qr_code: str,
) -> Any:
    """
    Login using QR code.
    """
    operario = db.query(Operario).filter(Operario.codigo_qr == qr_code).first()
    if not operario or not operario.activo:
        raise HTTPException(
            status_code=400,
            detail="Invalid QR code or inactive operator"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            {"sub": str(operario.id)}, access_token_expires
        ),
        "token_type": "bearer",
    }
