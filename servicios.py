from abc import abstractmethod
from entidades import Entidad
from excepciones import (
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class Servicio(Entidad):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if tarifa_base is None or tarifa_base <= 0:
            raise DatosInvalidosError(f"La tarifa base ({tarifa_base}) debe ser mayor a cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros_operacion(self, duracion_horas: int):
        """Valida reglas específicas de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Método polimórfico y sobrecargado mediante parámetros opcionales:
        - Puede llamarse solo con (duracion_horas)
        - Con descuento: (duracion_horas, descuento=0.10)
        - Con descuento e impuesto personalizado: (duracion_horas, descuento=0.10, impuesto=0.19)
        """
        pass

    def _aplicar_impuestos_y_descuentos(self, subtotal: float, descuento: float, impuesto: float) -> float:
        """Valida y aplica variaciones financieras evitando cálculos inconsistentes."""
        if not (0.0 <= descuento < 1.0):
            raise CalculoInconsistenteError(f"Descuento fuera de rango lógico (0 a 0.99): {descuento}")
        if not (0.0 <= impuesto <= 0.50):
            raise CalculoInconsistenteError(f"Impuesto fuera de rango lógico (0 a 0.50): {impuesto}")

        con_descuento = subtotal * (1 - descuento)
        total = con_descuento * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El cálculo final resultó en un valor negativo.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio especializado 1: Alquiler de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if capacidad is None or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a 0 personas.")
        self.__capacidad = capacidad

    def validar_parametros_operacion(self, duracion_horas: int):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"La sala '{self._nombre}' no está disponible actualmente.")
        if duracion_horas < 1 or duracion_horas > 12:
            raise DatosInvalidosError("La reserva de sala debe ser entre 1 y 12 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros_operacion(duracion_horas)
        subtotal = self._tarifa_base * duracion_horas
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self._disponible else "Ocupada"
        return f"Sala [{self.id}]: {self._nombre} (Cap: {self.__capacidad} pers.) - ${self._tarifa_base}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de hardware, servidores o equipos audiovisuales."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, deposito_seguridad: float, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if deposito_seguridad is None or deposito_seguridad < 0:
            raise DatosInvalidosError("El depósito de seguridad no puede ser negativo.")
        self.__deposito = float(deposito_seguridad)

    def validar_parametros_operacion(self, duracion_horas: int):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self._nombre}' ya se encuentra alquilado.")
        if duracion_horas < 2:
            raise DatosInvalidosError("El alquiler mínimo de equipos es de 2 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros_operacion(duracion_horas)
        subtotal = (self._tarifa_base * duracion_horas) + self.__deposito
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self._disponible else "Alquilado"
        return f"Equipo [{self.id}]: {self._nombre} - ${self._tarifa_base}/h + Depósito ${self.__deposito} [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Consultoría de software, redes o arquitectura."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not especialidad or not especialidad.strip():
            raise ParametroFaltanteError("Debe indicar el área de especialidad de la asesoría.")
        self.__especialidad = especialidad.strip()

    def validar_parametros_operacion(self, duracion_horas: int):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El consultor de '{self.__especialidad}' no tiene agenda disponible.")
        if duracion_horas <= 0:
            raise DatosInvalidosError("La duración de la asesoría debe ser mayor a 0 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros_operacion(duracion_horas)
        subtotal = self._tarifa_base * duracion_horas
        if duracion_horas > 5:
            subtotal *= 1.10
        return self._aplicar_impuestos_y_descuentos(subtotal, descuento, impuesto)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Asesoría [{self.id}]: {self._nombre} ({self.__especialidad}) - ${self._tarifa_base}/h [{estado}]"