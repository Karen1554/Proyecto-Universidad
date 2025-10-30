from fastapi import FastAPI
from db import create_db_and_tables
from estudiantes import estudiantes_router
from cursos import cursos_router
from matricula import matriculas_router

app = FastAPI(title="API Universidad", version="1.0")

@app.on_event("startup")
def startup_event():
    create_db_and_tables()

app.include_router(estudiantes_router)
app.include_router(cursos_router)
app.include_router(matriculas_router)
