from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from models import Estudiante
from db import engine

estudiantes_router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@estudiantes_router.post("/", status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: Estudiante):
    with Session(engine) as session:
        # Validar cédula única
        existente = session.exec(select(Estudiante).where(Estudiante.cedula == estudiante.cedula)).first()
        if existente:
            raise HTTPException(status_code=409, detail="Ya existe un estudiante con esta cédula.")
        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)
        return estudiante


@estudiantes_router.get("/")
def listar_estudiantes(semestre: int | None = None):
    with Session(engine) as session:
        query = select(Estudiante)
        if semestre:
            query = query.where(Estudiante.semestre == semestre)
        return session.exec(query).all()


@estudiantes_router.get("/{id}")
def obtener_estudiante(id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return estudiante


@estudiantes_router.put("/{id}")
def actualizar_estudiante(id: int, data: Estudiante):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        for campo, valor in data.dict(exclude_unset=True).items():
            setattr(estudiante, campo, valor)
        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)
        return estudiante


@estudiantes_router.delete("/{id}")
def eliminar_estudiante(id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        session.delete(estudiante)
        session.commit()
        return {"detail": "Estudiante eliminado correctamente"}
