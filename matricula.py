from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from models import Matricula, Estudiante, Curso
from db import engine

matriculas_router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

@matriculas_router.post("/", status_code=status.HTTP_201_CREATED)
def crear_matricula(matricula: Matricula):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, matricula.estudiante_id)
        curso = session.get(Curso, matricula.curso_id)
        if not estudiante or not curso:
            raise HTTPException(status_code=400, detail="Estudiante o curso inexistente")

        existente = session.exec(
            select(Matricula).where(
                Matricula.estudiante_id == matricula.estudiante_id,
                Matricula.curso_id == matricula.curso_id
            )
        ).first()
        if existente:
            raise HTTPException(status_code=409, detail="El estudiante ya está matriculado en este curso.")

        session.add(matricula)
        session.commit()
        session.refresh(matricula)
        return matricula


@matriculas_router.delete("/{id}")
def desmatricular(id: int):
    with Session(engine) as session:
        matricula = session.get(Matricula, id)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula no encontrada")
        session.delete(matricula)
        session.commit()
        return {"detail": "Matrícula eliminada correctamente"}


@matriculas_router.get("/curso/{curso_id}")
def estudiantes_en_curso(curso_id: int):
    with Session(engine) as session:
        curso = session.get(Curso, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        return [m.estudiante for m in curso.matriculas]


@matriculas_router.get("/estudiante/{estudiante_id}")
def cursos_de_estudiante(estudiante_id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return [m.curso for m in estudiante.matriculas]
