import logging
from excepciones import ErrorSistemaFJ
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import GestorSistemaFJ

logging.basicConfig(
    filename="sistema_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)


def ejecutar_simulacion():
    print("=== INICIANDO SISTEMA INTEGRAL SOFTWARE FJ ===\n")
    logging.info("=== INICIO DE EJECUCIÓN DEL SISTEMA SOFTWARE FJ ===")
    sistema = GestorSistemaFJ()

    # OP 1: Registro válido de Cliente 1 (try / except / else)
    try:
        c1 = Cliente("CLI-01", "Laura Martínez", "laura.m@empresa.com", "3104567890")
        sistema.registrar_cliente(c1)
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 1] Error registrando cliente: {e}")
        print(f"[OP 1] Error: {e}")
    else:
        print(f"[OP 1] Éxito -> {c1.obtener_resumen()}")

    # OP 2: Registro válido de Cliente 2
    try:
        c2 = Cliente("CLI-02", "Carlos Mendoza", "cmendoza@tech.co", "3209876543")
        sistema.registrar_cliente(c2)
        print(f"[OP 2] Éxito -> {c2.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 2] Error registrando cliente: {e}")

    # OP 3: Registro INVÁLIDO de Cliente (correo mal formado)
    try:
        c_malo = Cliente("CLI-03", "Pedro", "correo_sin_arroba.com", "3001112233")
        sistema.registrar_cliente(c_malo)
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 3] Validación de cliente capturada: {e}")
        print(f"[OP 3] Error controlado -> {e}")

    # OP 4: Registro INVÁLIDO de Cliente (teléfono con letras)
    try:
        c_tel_malo = Cliente("CLI-04", "Ana Gómez", "ana@dominio.com", "315ABC99")
        sistema.registrar_cliente(c_tel_malo)
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 4] Validación de teléfono capturada: {e}")
        print(f"[OP 4] Error controlado -> {e}")

    # OP 5: Creación válida de 3 Servicios Especializados
    try:
        s1 = ReservaSala("SRV-01", "Sala Juntas Innovación", 50000, capacidad=12)
        s2 = AlquilerEquipo("SRV-02", "Servidor Dell PowerEdge", 35000, deposito_seguridad=100000)
        s3 = AsesoriaEspecializada("SRV-03", "Auditoría Ciberseguridad", 120000, especialidad="Seguridad Informática")
        sistema.registrar_servicio(s1)
        sistema.registrar_servicio(s2)
        sistema.registrar_servicio(s3)
        print("[OP 5] Éxito -> 3 servicios especializados creados y registrados.")
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 5] Error creando servicios: {e}")

    # OP 6: Creación INCORRECTA de Servicio (tarifa negativa)
    try:
        s_malo = ReservaSala("SRV-04", "Sala Fantasma", -25000, capacidad=5)
        sistema.registrar_servicio(s_malo)
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 6] Error en creación de servicio: {e}")
        print(f"[OP 6] Error controlado -> {e}")

    # OP 7: Reserva EXITOSA de Sala (try / except / else / finally)
    try:
        r1 = sistema.crear_reserva("RES-01", "CLI-01", "SRV-01", duracion=4)
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 7] Error en reserva: {e}")
    else:
        print(f"[OP 7] Éxito -> {r1.obtener_resumen()}")
    finally:
        logging.info("[OP 7] Bloque finally ejecutado tras intento de reserva RES-01.")

    # OP 8: Reserva FALLIDA (Sala ya ocupada por OP 7)
    try:
        r2 = sistema.crear_reserva("RES-02", "CLI-02", "SRV-01", duracion=2)
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 8] Intento de reserva sobre recurso ocupado: {e}")
        print(f"[OP 8] Error controlado -> {e}")

    # OP 9: Reserva EXITOSA de Equipo (método sobrecargado con 15% descuento)
    try:
        r3 = sistema.crear_reserva("RES-03", "CLI-02", "SRV-02", duracion=5, descuento=0.15)
        print(f"[OP 9] Éxito (con 15% dcto) -> {r3.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 9] Error en alquiler de equipo: {e}")

    # OP 10: Reserva FALLIDA por cálculo inconsistente (descuento del 150%)
    try:
        r4 = sistema.crear_reserva("RES-04", "CLI-01", "SRV-03", duracion=3, descuento=1.50)
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 10] Cálculo inconsistente bloqueado: {e}")
        print(f"[OP 10] Error controlado -> {e}")

    # OP 11: Reserva FALLIDA con ENCADENAMIENTO DE EXCEPCIONES (cliente inexistente)
    try:
        r5 = sistema.crear_reserva("RES-05", "CLI-999", "SRV-03", duracion=3)
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 11] {e} | Causa original encadenada: {repr(e.__cause__)}")
        print(f"[OP 11] Error encadenado -> {e} (Causa: {e.__cause__})")

    # OP 12: Cancelación de reserva (RES-01) y nueva reserva exitosa sobre la sala liberada
    try:
        r1.cancelar()
        logging.info(f"[OP 12] Reserva {r1.id} cancelada. Sala liberada.")
        r6 = sistema.crear_reserva("RES-06", "CLI-02", "SRV-01", duracion=3, descuento=0.10, impuesto=0.0)
        print(f"[OP 12] Éxito tras cancelación -> {r6.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logging.error(f"[OP 12] Error en flujo de cancelación/re-reserva: {e}")

    print("\n=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ===")
    print("Revise el archivo 'sistema_fj.log' para ver la auditoría completa.")
    logging.info("=== FIN DE EJECUCIÓN DEL SISTEMA SOFTWARE FJ ===")


if __name__ == "__main__":
    ejecutar_simulacion()