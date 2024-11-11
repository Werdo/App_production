# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Generator, Optional
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.operario import Operario

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_operario(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Optional[Operario]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        operario_id: int = payload.get("sub")
        if operario_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    operario = db.query(Operario).filter(Operario.id == operario_id).first()
    if operario is None:
        raise credentials_exception
    return operario
