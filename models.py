from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class EntradaBase(BaseModel):
    Evento: str = Field(
        ...,
        min_length = 2,
        max_length = 100,
        description = "Nombre del Evento",
        example = "Rock Al Parque"
    )
    zona_asiento: str = Field(
        ...,
        min_length=1,
        max_length = 15,
        description="Zona de la Entrada",
        example="A2, VIP, Basica"
    )
    precio_entrada: float = Field(
        ...,
        gt=0,
        description="Precio de la Entrada",

    )
    pagada: bool = Field(
        default=False,
        description="Estado del pago de la Entrada"
    )

class EntradaCreate(EntradaBase):
    pass

class EntradaUpdate(BaseModel):
    Evento: Optional[str] = Field(None, min_length=2, max_length=100)
    zona_asiento: Optional[str] = Field(None, min_length = 1, max_length= 15)
    precio_entrada: Optional[float]= Field(None,gt=0)
    pagada: Optional[bool] = None

class Entrada(EntradaBase):
    id: UUID = Field(default_factory=uuid4, description="Identificador Unico Universal (UUIDv4)")

    class Config:
        from_attributes = True