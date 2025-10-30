from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Matricula(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiante.id")
    curso_id: int = Field(foreign_key="curso.id")

    estudiante: Optional["Estudiante"] = Relationship(back_populates="matriculas")
    curso: Optional["Curso"] = Relationship(back_populates="matriculas")


class Estudiante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cedula: str = Field(index=True, unique=True, nullable=False)
    nombre: str
    email: str
    semestre: int

    matriculas: List[Matricula] = Relationship(back_populates="estudiante")


class Curso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(index=True, unique=True, nullable=False)
    nombre: str
    creditos: int
    horario: str

    matriculas: List[Matricula] = Relationship(back_populates="curso")
