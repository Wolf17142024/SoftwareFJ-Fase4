from abc import ABC, abstractmethod
import re
from excepciones import DatosInvalidosError, ParametroFaltanteError


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, id_entidad: str):
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ParametroFaltanteError("El ID de la entidad no puede estar vacío.")
        self._id = id_entidad.strip()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio para describir la entidad."""
        pass


class Cliente(Entidad):
    """Representa a un cliente de Software FJ con datos personales encapsulados."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError(f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not re.match(patron, valor.strip()):
            raise DatosInvalidosError(f"Correo electrónico inválido: '{valor}'.")
        self.__correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.strip().isdigit() or len(valor.strip()) < 7:
            raise DatosInvalidosError(f"Teléfono inválido: '{valor}'. Debe contener solo números (mín. 7 dígitos).")
        self.__telefono = valor.strip()

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id}] - {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"