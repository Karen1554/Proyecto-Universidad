from fastapi import APIRouter
from sqlmodel import Session, select
from models import Curso
from db import engine

cursos_router = APIRouter(prefix="/cursos", tags=["Cursos"])

@cursos_router.post("/")
def crear_curso(curso: Curso):
    with Session(engine) as session:
        session.add(curso)
        session.commit()
        session.refresh(curso)
        return curso

@cursos_router.get("/")
def listar_cursos():
    with Session(engine) as session:
        return session.exec(select(Curso)).all()
