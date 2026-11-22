class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores controlados de Software FJ."""
    pass


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando los datos ingresados no cumplen el formato o están vacíos."""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un argumento obligatorio o es nulo."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando el servicio o equipo no está disponible para reservar."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza ante intentos de reserva incorrectos, duraciones negativas o estados inválidos."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo de costo, descuento o impuesto arroja un valor ilógico."""
    pass