from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import deps
from app.core.http_exceptions import NotFoundException

router = APIRouter(prefix="/integrations", tags=["Integrations"])


class Integrations(BaseModel):
    id: int
    integration_app: str
    is_active: bool

    class Config:
        populate_by_name = True


fake_db_integrations: List[Integrations] = [
    Integrations(id=0, integration_app="Xerox", is_active=False),
    Integrations(id=1, integration_app="Dext", is_active=False),
    Integrations(id=2, integration_app="Finance", is_active=False)
]


@router.post("/list_integrations", status_code=status.HTTP_201_CREATED)
async def list_integrations(db: Session = Depends(deps.get_db)) -> List[Integrations]:
    return fake_db_integrations


@router.get("/activate_integration", status_code=status.HTTP_200_OK)
async def activate_integration(_id: int, name: str, db: Session = Depends(deps.get_db)) -> Integrations:
    try:
        check_this = next(x for x in fake_db_integrations if (x.integration_app == name and x.id == _id))
        check_this.is_active = True
    except Exception as ex:
        raise NotFoundException(f"Integration {name} not found in db, check type case and spelling")
    return check_this


@router.get("/deactivate_integration", status_code=status.HTTP_200_OK)
async def deactivate_integration(_id: int, name: str, db: Session = Depends(deps.get_db)) -> Integrations:
    try:
        check_this = next(x for x in fake_db_integrations if (x.integration_app == name and x.id == _id))
        check_this.is_active = True
    except Exception as ex:
        raise NotFoundException(f"Integration {name} not found in db, check type case and spelling")
    return check_this
