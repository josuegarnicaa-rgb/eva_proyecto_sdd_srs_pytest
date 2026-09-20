from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Prestamo:
    id: int
    usuario_id: int
    equipo_id: int
    fecha_prestamo: str
    fecha_devolucion: str
    estado: str