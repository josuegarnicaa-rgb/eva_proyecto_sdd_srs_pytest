from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Usuario:
    id: int
    nombre: str
    apellido: str
    correo: str