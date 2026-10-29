from typing import List
from models import Entrada
from uuid import uuid4

db_entradas: List[Entrada] = []

def cargar_datos_iniciales():
    if not db_entradas:
        db_entradas.extend([
            Entrada(
                id=uuid4(),
                Evento="Rock Al Parque",
                zona_asiento="VIP",
                precio_entrada=80000.0,
                pagada=False
            ),
            Entrada(
                id=uuid4(),
                Evento="Salsa Al Parque",
                zona_asiento="A1",
                precio_entrada=50000.0,
                pagada=True
            )
        ])