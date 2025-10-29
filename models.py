from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class Estudiante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    edad: int

    matriculas: List["Matricula"] = Relationship(back_populates="estudiante")


class Curso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    codigo: str
    creditos: int

    matriculas: List["Matricula"] = Relationship(back_populates="curso")


class Matricula(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiante.id")
    curso_id: int = Field(foreign_key="curso.id")
    fecha: date

    estudiante: Optional[Estudiante] = Relationship(back_populates="matriculas")
    curso: Optional[Curso] = Relationship(back_populates="matriculas")
