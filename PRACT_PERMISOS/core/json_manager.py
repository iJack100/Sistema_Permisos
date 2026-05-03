import json
import os


class JsonManager:
    """
    Gestiona la persistencia de datos en archivos JSON.
    Cada colección (empleados, tipos_permisos, permisos) tiene su propio archivo.
    """

    BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

    @classmethod
    def _ruta(cls, nombre_archivo: str) -> str:
        return os.path.join(cls.BASE_DIR, nombre_archivo)

    @classmethod
    def leer(cls, nombre_archivo: str) -> list:
        """Lee y devuelve la lista de registros del archivo JSON."""
        ruta = cls._ruta(nombre_archivo)
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def escribir(cls, nombre_archivo: str, datos: list) -> None:
        """Serializa y guarda la lista completa en el archivo JSON."""
        ruta = cls._ruta(nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
