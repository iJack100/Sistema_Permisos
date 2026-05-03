from abc import ABC, abstractmethod


class ICrud(ABC):
    """Interfaz base que define las operaciones CRUD completas."""

    @abstractmethod
    def crear(self):
        """C — Registra un nuevo elemento."""
        pass

    @abstractmethod
    def consultar(self):
        """R — Lista todos los elementos."""
        pass

    @abstractmethod
    def buscar(self, id: int):
        """R — Busca y muestra un elemento por su ID."""
        pass

    @abstractmethod
    def actualizar(self, id: int):
        """U — Modifica los datos de un elemento existente."""
        pass

    @abstractmethod
    def eliminar(self):
        """D — Elimina un elemento por su ID."""
        pass
