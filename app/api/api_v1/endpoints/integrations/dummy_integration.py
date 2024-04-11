from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from app.api import deps

router = APIRouter(prefix="/integrations", tags=["Integrations"])


class Integrations(BaseModel):
    id: int
    integration_app: str

    class Config:
        populate_by_name = True


fake_db_integrations: List[Integrations] = [
    Integrations(id=0, integration_app="Xerox"),
    Integrations(id=1, integration_app="Dext"),
    Integrations(id=2, integration_app="Finance")
]


@router.post("/list_integrations", status_code=status.HTTP_201_CREATED)
async def list_integrations(db: Session = Depends(deps.get_db)) -> List[Integrations]:
    return fake_db_integrations


@router.get("/activate_integration", status_code=status.HTTP_200_OK)
async def activate_integration(_id: int, name: str, db: Session = Depends(deps.get_db)) -> bool:
    check_this = Integrations(id=_id, integration_app=name),

    if check_this in fake_db_integrations:
        return True
    else:
        return False
