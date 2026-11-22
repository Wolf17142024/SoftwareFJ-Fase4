import logging
from entidades import Entidad, Cliente
from servicios import Servicio
from excepciones import (
    ParametroFaltanteError,
    ReservaInvalidaError,
)


class Reserva(Entidad):
    """Integra Cliente, Servicio, duración y estado de la reserva."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise ParametroFaltanteError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ParametroFaltanteError("Se requiere una instancia válida de Servicio.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ReservaInvalidaError(f"Duración inválida ({duracion_horas}h). Debe ser un entero positivo.")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion_horas
        self.__estado = "PENDIENTE"
        self.__costo_total = 0.0

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    def procesar_y_confirmar(self, descuento: float = 0.0, impuesto: float = 0.19):
        """Calcula el costo, bloquea el servicio y cambia el estado a CONFIRMADA."""
        if self.__estado != "PENDIENTE":
            raise ReservaInvalidaError(f"No se puede confirmar la reserva {self.id} en estado '{self.__estado}'.")

        self.__costo_total = self.__servicio.calcular_costo(self.__duracion, descuento, impuesto)
        self.__servicio.disponible = False
        self.__estado = "CONFIRMADA"

    def cancelar(self):
        """Cancela la reserva y libera el servicio si estaba confirmada."""
        if self.__estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id} ya se encuentra cancelada.")
        if self.__estado == "CONFIRMADA":
            self.__servicio.disponible = True
        self.__estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Estado: {self.__estado} | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion}h | Total: ${self.__costo_total:,.2f}"
        )


class GestorSistemaFJ:
    """Administra en memoria (listas) los clientes, servicios y reservas de Software FJ."""

    def __init__(self):
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, cliente: Cliente):
        if any(c.id == cliente.id for c in self.clientes):
            raise ReservaInvalidaError(f"Ya existe un cliente registrado con el ID '{cliente.id}'.")
        self.clientes.append(cliente)
        logging.info(f"Cliente registrado exitosamente: {cliente.obtener_resumen()}")

    def registrar_servicio(self, servicio: Servicio):
        if any(s.id == servicio.id for s in self.servicios):
            raise ReservaInvalidaError(f"Ya existe un servicio registrado con el ID '{servicio.id}'.")
        self.servicios.append(servicio)
        logging.info(f"Servicio registrado exitosamente: {servicio.obtener_resumen()}")

    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion: int,
        descuento: float = 0.0,
        impuesto: float = 0.19,
    ) -> Reserva:
        """Busca entidades y procesa la reserva aplicando encadenamiento de excepciones."""
        try:
            cliente = next((c for c in self.clientes if c.id == id_cliente), None)
            if cliente is None:
                raise KeyError(f"ID de cliente '{id_cliente}' no encontrado en el listado.")

            servicio = next((s for s in self.servicios if s.id == id_servicio), None)
            if servicio is None:
                raise KeyError(f"ID de servicio '{id_servicio}' no encontrado en el catálogo.")

            reserva = Reserva(id_reserva, cliente, servicio, duracion)
            reserva.procesar_y_confirmar(descuento=descuento, impuesto=impuesto)
            self.reservas.append(reserva)
            logging.info(f"Reserva confirmada: {reserva.obtener_resumen()}")
            return reserva

        except KeyError as e:
            raise ReservaInvalidaError(f"Fallo al vincular entidades en la reserva '{id_reserva}'.") from e