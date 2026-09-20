from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Equipo:
    id: int
    nombre: str
    codigo: str
    descripcion: str
    estado: str