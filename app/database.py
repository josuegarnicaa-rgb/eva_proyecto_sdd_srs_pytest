import sqlite3
from pathlib import Path


# Ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta donde se almacenará la base de datos
DATA_DIR = BASE_DIR / "data"

# Base de datos principal
DATABASE_PATH = DATA_DIR / "prestamos.db"


def get_connection(database_path=DATABASE_PATH):
    """
    Crea y devuelve una conexión a SQLite.
    """

    # Crear la carpeta data si todavía no existe
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(str(database_path))

    # Permite acceder a las columnas por nombre
    connection.row_factory = sqlite3.Row

    # Activar claves foráneas en SQLite
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables(connection):
    """
    Crea las tablas necesarias para el sistema.
    """

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            first_name TEXT NOT NULL
                CHECK (
                    length(trim(first_name)) BETWEEN 2 AND 50
                ),

            last_name TEXT NOT NULL
                CHECK (
                    length(trim(last_name)) BETWEEN 2 AND 50
                ),

            email TEXT NOT NULL UNIQUE
                CHECK (
                    length(email) <= 100
                )
        );


        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL
                CHECK (
                    length(trim(name)) BETWEEN 2 AND 80
                ),

            code TEXT NOT NULL UNIQUE
                CHECK (
                    length(code) BETWEEN 3 AND 10
                ),

            description TEXT NOT NULL
                CHECK (
                    length(description) <= 250
                ),

            status TEXT NOT NULL DEFAULT 'DISPONIBLE'
                CHECK (
                    status IN ('DISPONIBLE', 'PRESTADO')
                )
        );


        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            equipment_id INTEGER NOT NULL,

            loan_date TEXT NOT NULL,

            return_date TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'ACTIVO'
                CHECK (
                    status IN ('ACTIVO', 'DEVUELTO', 'ATRASADO')
                ),

            FOREIGN KEY (user_id)
                REFERENCES users(id),

            FOREIGN KEY (equipment_id)
                REFERENCES equipment(id)
        );


        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_equipment_active_loan
        ON loans(equipment_id)
        WHERE status IN ('ACTIVO', 'ATRASADO');
        """
    )

    connection.commit()


def initialize_database():
    """
    Inicializa la base de datos principal del sistema.
    """

    connection = get_connection()

    try:
        create_tables(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

    print(f"Base de datos creada correctamente en:")
    print(DATABASE_PATH)