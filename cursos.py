from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from models import Curso
from db import engine

cursos_router = APIRouter(prefix="/cursos", tags=["Cursos"])

@cursos_router.post("/", status_code=status.HTTP_201_CREATED)
def crear_curso(curso: Curso):
    with Session(engine) as session:
        existente = session.exec(select(Curso).where(Curso.codigo == curso.codigo)).first()
        if existente:
            raise HTTPException(status_code=409, detail="Ya existe un curso con este código.")
        session.add(curso)
        session.commit()
        session.refresh(curso)
        return curso


@cursos_router.get("/")
def listar_cursos(creditos: int | None = None, codigo: str | None = None):
    with Session(engine) as session:
        query = select(Curso)
        if creditos:
            query = query.where(Curso.creditos == creditos)
        if codigo:
            query = query.where(Curso.codigo == codigo)
        return session.exec(query).all()


@cursos_router.get("/{id}")
def obtener_curso(id: int):
    with Session(engine) as session:
        curso = session.get(Curso, id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        return curso


@cursos_router.put("/{id}")
def actualizar_curso(id: int, data: Curso):
    with Session(engine) as session:
        curso = session.get(Curso, id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        for campo, valor in data.dict(exclude_unset=True).items():
            setattr(curso, campo, valor)
        session.add(curso)
        session.commit()
        session.refresh(curso)
        return curso


@cursos_router.delete("/{id}")
def eliminar_curso(id: int):
    with Session(engine) as session:
        curso = session.get(Curso, id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        session.delete(curso)
        session.commit()
        return {"detail": "Curso eliminado correctamente"}
