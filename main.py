from fastapi import FastAPI, HTTPException, status
from typing import List
from uuid import UUID

from models import Entrada,EntradaCreate, EntradaUpdate
from database import db_entradas, cargar_datos_iniciales

app =  FastAPI(
    title = "APIRestFull - Venta de Entradas Para Conciertos",
    description="API RESTful creada para la administracion de entradas para conciertos",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    cargar_datos_iniciales()

@app.get(
    "/",
    tags=["Raíz"],
    summary="Mensaje de Bienvenida"
)
def welcome():
    return{
        "mensaje": "Bienvenido al panel de Administracion",
        "documentacion": "/docs"
    }


@app.get(
    "/entradas",
    response_model=List[Entrada],
    status_code=status.HTTP_200_OK,
    tags=["Entradas"],
    summary="Obtener todas las entradas registradas."
)
def get_entradas():
    return db_entradas

@app.get(
    "/entradas/{entrada_id}",
    response_model=Entrada,
    status_code=status.HTTP_200_OK,
    tags=["Entradas"],
    summary="Buscar entradas por su ID."
)
def get_entrada_por_id(entrada_id: UUID):
    for entrada in db_entradas:
        if entrada.id == entrada_id:
            return entrada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"La entrada con el ID {entrada_id} no ha sido encontrada."
    )

@app.post(
    "/entradas",
    response_model=Entrada,
    status_code=status.HTTP_201_CREATED,
    tags=["Entradas"],
    summary="Registre una nueva entrada"
)
def create_entrada(entrada_in: EntradaCreate):
    for entrada in db_entradas:
        if entrada.zona_asiento.lower() == entrada_in.zona_asiento.lower() and entrada.Evento.lower() == entrada_in.Evento.lower():
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una entrada registrada para el asiento '{entrada_in.zona_asiento}' en el evento de '{entrada.Evento}'."
            )
    
    nueva_entrada = Entrada(**entrada_in.model_dump())
    db_entradas.append(nueva_entrada)
    return nueva_entrada

@app.put(
    "/entrada/{entrada_id}",
    response_model=Entrada,
    status_code=status.HTTP_200_OK,
    tags=["Entradas"],
    summary="Actualizar informacion de la Entrada por su ID"
)

def update_entrada(entrada_id: UUID,entrada_update:EntradaUpdate):
    for index, entrada in enumerate(db_entradas):
        if entrada.id == entrada_id:
            datos_actualizados = entrada_update.model_dump(exclude_unset=True)

            entrada_modificada = entrada.model_copy(update=datos_actualizados)
            db_entradas[index] = entrada_modificada
            return entrada_modificada

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No es posible actualizar la entrada ya que el ID '{entrada_id}' no existe."
        )

@app.delete(
    "/entradas/{entrada_id}",
    status_code=status.HTTP_200_OK,
    tags=["Entradas"],
    summary="Eliminar entrada por su ID"
)

def delete_entrada(entrada_id: UUID):
    for index, entrada in enumerate(db_entradas):
        if entrada.id == entrada_id:
            entrada_eliminada = db_entradas.pop(index)
            return{
                "mensaje": "Entrada eliminada exitosamente",
                "entrada_eliminado": entrada_eliminada
            }

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No es posible eliminar la entrada con el ID '{entrada_id}' porque no existe."
        )