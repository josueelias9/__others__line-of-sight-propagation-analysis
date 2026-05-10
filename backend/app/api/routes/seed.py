from fastapi import APIRouter

from app.api.deps import CurrentUserIdDep
from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.csv_data_loader import load_csv_data
from application.use_cases.poblar_datos_usuario import (
    PoblarDatosUsuarioUseCase,
    PoblarDatosUsuarioRequest,
)
from app.models import UserTable
from sqlmodel import select

router = APIRouter()


@router.post("", status_code=200)
def post_seed(session: SessionDep, user_id: CurrentUserIdDep):
    """Popula los datos de plantilla (puntos de ejemplo) para el usuario actual."""
    user = session.exec(select(UserTable).where(UserTable.id == user_id)).first()
    if user is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    use_case = PoblarDatosUsuarioUseCase(session=session, data_loader=load_csv_data)
    response = use_case.ejecutar(PoblarDatosUsuarioRequest(email=user.email))
    return {"puntos_creados": response.puntos_creados}
