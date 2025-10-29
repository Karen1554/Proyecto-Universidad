from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import Matricula, Estudiante, Curso
from db import engine

matricula_router = APIRouter(prefix="/matriculas", tags=["Matriculas"])

@matricula_router.post("/")
def crear_matricula(matricula: Matricula):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, matricula.estudiante_id)
        curso = session.get(Curso, matricula.curso_id)
        if not estudiante or not curso:
            raise HTTPException(status_code=400, detail="Estudiante o curso inexistente")

        session.add(matricula)
        session.commit()
        session.refresh(matricula)
        return matricula

@matricula_router.get("/")
def listar_matriculas():
    with Session(engine) as session:
        return session.exec(select(Matricula)).all()
