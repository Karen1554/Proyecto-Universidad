from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import Estudiante
from db import engine

estudiantes_router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@estudiantes_router.post("/")
def crear_estudiante(estudiante: Estudiante):
    with Session(engine) as session:
        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)
        return estudiante

@estudiantes_router.get("/")
def listar_estudiantes():
    with Session(engine) as session:
        return session.exec(select(Estudiante)).all()

@estudiantes_router.get("/{id}")
def obtener_estudiante(id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return estudiante
