# ==============================================================
# UNAD - Curso: Programacion (213023)
# Fase 4 - Practicas simuladas
# Ejercicio 1: Sistema Integral de Clientes, Servicios y Reservas
# Estudiante: Manuel Octavio Echavarria Granados
# Grupo: 213023_228
# ==============================================================

# ABC y abstractmethod permiten declarar clases abstractas.
from abc import ABC, abstractmethod
# datetime permite indicar la fecha y hora de cada registro.
from datetime import datetime


# ==============================================================
# REGISTRO DE EVENTOS Y ERRORES
# ==============================================================
def guardar_registro(tipo, detalle):
    # Los registros se guardan en un archivo de texto, no en una base de datos.
    try:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("registro_software_fj.txt", "a", encoding="utf-8") as archivo:
            archivo.write(fecha + " | " + tipo + " | " + detalle + "\n")
    except OSError:
        # Si el archivo no se puede escribir, el programa sigue funcionando.
        print("Aviso: no se pudo guardar el registro en el archivo.")


# ==============================================================
# EXCEPCIONES PERSONALIZADAS
# ==============================================================
class ErrorSistema(Exception):
    pass


class DatoInvalidoError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class OperacionNoPermitidaError(ErrorSistema):
    pass


# Convierte un dato a numero y verifica que sea mayor que cero.
def numero_positivo(valor, campo):
    try:
        numero = float(valor)
    except (ValueError, TypeError) as error:
        # "from error" conserva la causa original de la excepcion.
        raise DatoInvalidoError(campo + ": debe ingresar un numero valido.") from error
    if numero <= 0 or numero == float("inf") or numero != numero:
        raise DatoInvalidoError(campo + ": el numero debe ser mayor que cero.")
    return numero


# ==============================================================
# CLASE ABSTRACTA: Entidad
# ==============================================================
class Entidad(ABC):
    @abstractmethod
    def descripcion(self):
        pass


# ==============================================================
# CLASE Cliente (encapsulacion y validacion)
# ==============================================================
class Cliente(Entidad):
    def __init__(self, nombre, identificacion, correo):
        if not isinstance(nombre, str) or nombre.strip() == "":
            raise DatoInvalidoError("El nombre del cliente es obligatorio.")
        if not str(identificacion).isdigit() or int(identificacion) <= 0:
            raise DatoInvalidoError("La identificacion debe contener numeros positivos.")
        if (not isinstance(correo, str) or correo.count("@") != 1
                or "." not in correo.split("@")[1] or " " in correo):
            raise DatoInvalidoError("El correo electronico no es valido.")

        # Atributos privados: igual que en los trabajos anteriores.
        self._nombre = nombre.strip()
        self._identificacion = str(identificacion)
        self._correo = correo.strip()

    def obtener_identificacion(self):
        return self._identificacion

    def descripcion(self):
        return self._nombre + " | ID: " + self._identificacion


# ==============================================================
# CLASE ABSTRACTA: Servicio
# ==============================================================
class Servicio(Entidad):
    def __init__(self, nombre, tarifa):
        if not isinstance(nombre, str) or nombre.strip() == "":
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")
        self._nombre = nombre.strip()
        self._tarifa = numero_positivo(tarifa, "Tarifa")
        self._disponible = True

    def obtener_nombre(self):
        return self._nombre

    def esta_disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        self._disponible = disponible
        guardar_registro("EVENTO", self._nombre + " - Disponible: " + str(disponible))

    # Se simula sobrecarga usando parametros opcionales, como en Fase 3.
    def aplicar_ajustes(self, subtotal, descuento=0, impuesto=0):
        try:
            descuento = float(descuento)
            impuesto = float(impuesto)
        except (ValueError, TypeError) as error:
            raise DatoInvalidoError("Descuento e impuesto deben ser numeros.") from error
        if (descuento < 0 or descuento > 100 or impuesto < 0 or impuesto > 100
                or descuento != descuento or impuesto != impuesto):
            raise DatoInvalidoError("Descuento e impuesto deben estar entre 0 y 100.")
        total = subtotal - subtotal * descuento / 100
        total = total + total * impuesto / 100
        if total < 0:
            raise DatoInvalidoError("El costo calculado no puede ser negativo.")
        return total

    @abstractmethod
    def validar_parametros(self):
        pass

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass


# ==============================================================
# TRES CLASES HIJAS: herencia y polimorfismo
# ==============================================================
class ServicioSala(Servicio):
    def __init__(self, nombre, tarifa, capacidad):
        super().__init__(nombre, tarifa)
        self._capacidad = numero_positivo(capacidad, "Capacidad")
        self.validar_parametros()

    def validar_parametros(self):
        if not self._capacidad.is_integer():
            raise DatoInvalidoError("La capacidad de la sala debe ser entera.")

    def descripcion(self):
        return "Sala: " + self._nombre + " | Capacidad: " + str(int(self._capacidad))

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        subtotal = self._tarifa * numero_positivo(duracion, "Duracion")
        return self.aplicar_ajustes(subtotal, descuento, impuesto)


class ServicioEquipo(Servicio):
    def __init__(self, nombre, tarifa, cantidad):
        super().__init__(nombre, tarifa)
        self._cantidad = numero_positivo(cantidad, "Cantidad")
        self.validar_parametros()

    def validar_parametros(self):
        if not self._cantidad.is_integer():
            raise DatoInvalidoError("La cantidad de equipos debe ser entera.")

    def descripcion(self):
        return "Equipo: " + self._nombre + " | Unidades: " + str(int(self._cantidad))

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        # El alquiler cobra por hora y por cantidad de equipos.
        subtotal = self._tarifa * numero_positivo(duracion, "Duracion") * self._cantidad
        return self.aplicar_ajustes(subtotal, descuento, impuesto)


class ServicioAsesoria(Servicio):
    def __init__(self, nombre, tarifa, especialidad):
        super().__init__(nombre, tarifa)
        self._especialidad = especialidad
        self.validar_parametros()

    def validar_parametros(self):
        if not isinstance(self._especialidad, str) or self._especialidad.strip() == "":
            raise DatoInvalidoError("La especialidad es obligatoria.")

    def descripcion(self):
        return "Asesoria: " + self._nombre + " | Area: " + self._especialidad

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        subtotal = self._tarifa * numero_positivo(duracion, "Duracion")
        return self.aplicar_ajustes(subtotal, descuento, impuesto)


# ==============================================================
# CLASE Reserva: confirmar, cancelar y procesar
# ==============================================================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva necesita un cliente valido.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva necesita un servicio valido.")
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = numero_positivo(duracion, "Duracion")
        self._estado = "Pendiente"
        self._total = 0

    def confirmar(self):
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError("Solo se puede confirmar una reserva pendiente.")
        if not self._servicio.esta_disponible():
            raise ServicioNoDisponibleError("El servicio no esta disponible.")
        self._estado = "Confirmada"

    def cancelar(self):
        if self._estado != "Confirmada":
            raise OperacionNoPermitidaError("Solo se puede cancelar una reserva confirmada.")
        self._estado = "Cancelada"

    def procesar(self, descuento=0, impuesto=0):
        # try/except/else/finally mantiene el control cuando aparece un error.
        try:
            self.confirmar()
            total = self._servicio.calcular_costo(self._duracion, descuento, impuesto)
        except ErrorSistema as error:
            if self._estado == "Pendiente" or self._estado == "Confirmada":
                self._estado = "Fallida"
            print("ERROR en reserva:", error)
            guardar_registro("ERROR", "Reserva de " + self._servicio.obtener_nombre()
                             + ": " + str(error))
            return False
        else:
            self._total = total
            print("Reserva confirmada | Total: $" + str(round(total, 2)))
            guardar_registro("EXITO", "Reserva de " + self._servicio.obtener_nombre()
                             + " confirmada. Total: $" + str(round(total, 2)))
            return True
        finally:
            guardar_registro("EVENTO", "Procesamiento finalizado. Estado: " + self._estado)

    def obtener_estado(self):
        return self._estado


# ==============================================================
# CLASE PRINCIPAL: listas de clientes, servicios y reservas
# ==============================================================
class SistemaSoftwareFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    def registrar_cliente(self, nombre, identificacion, correo):
        try:
            cliente = Cliente(nombre, identificacion, correo)
            for registrado in self._clientes:
                if registrado.obtener_identificacion() == cliente.obtener_identificacion():
                    raise OperacionNoPermitidaError("Ya existe un cliente con esa identificacion.")
            self._clientes.append(cliente)
        except ErrorSistema as error:
            print("ERROR al registrar cliente:", error)
            guardar_registro("ERROR", "Registro de cliente: " + str(error))
            return None
        else:
            print("Cliente registrado:", cliente.descripcion())
            guardar_registro("EXITO", "Cliente registrado: " + cliente.descripcion())
            return cliente

    def crear_servicio(self, tipo, nombre, tarifa, adicional):
        try:
            if tipo == "sala":
                servicio = ServicioSala(nombre, tarifa, adicional)
            elif tipo == "equipo":
                servicio = ServicioEquipo(nombre, tarifa, adicional)
            elif tipo == "asesoria":
                servicio = ServicioAsesoria(nombre, tarifa, adicional)
            else:
                raise DatoInvalidoError("Tipo de servicio no reconocido.")
            self._servicios.append(servicio)
        except ErrorSistema as error:
            print("ERROR al crear servicio:", error)
            guardar_registro("ERROR", "Creacion de servicio: " + str(error))
            return None
        else:
            print("Servicio creado:", servicio.descripcion())
            guardar_registro("EXITO", "Servicio creado: " + servicio.descripcion())
            return servicio

    def realizar_reserva(self, cliente, servicio, duracion, descuento=0, impuesto=0):
        try:
            reserva = Reserva(cliente, servicio, duracion)
            self._reservas.append(reserva)
        except ErrorSistema as error:
            print("ERROR al crear reserva:", error)
            guardar_registro("ERROR", "Creacion de reserva: " + str(error))
            return None
        else:
            reserva.procesar(descuento, impuesto)
            return reserva

    def cancelar_reserva(self, reserva):
        try:
            if not isinstance(reserva, Reserva):
                raise DatoInvalidoError("La reserva indicada no existe.")
            reserva.cancelar()
        except ErrorSistema as error:
            print("ERROR al cancelar reserva:", error)
            guardar_registro("ERROR", "Cancelacion de reserva: " + str(error))
        else:
            print("Reserva cancelada correctamente.")
            guardar_registro("EXITO", "Reserva cancelada correctamente.")

    def mostrar_resumen(self):
        print("\nRESUMEN DEL SISTEMA SOFTWARE FJ")
        print("Clientes registrados:", len(self._clientes))
        print("Servicios creados:", len(self._servicios))
        print("Reservas realizadas:", len(self._reservas))
        for reserva in self._reservas:
            print("- Estado:", reserva.obtener_estado())


# ==============================================================
# SIMULACION: 18 OPERACIONES VALIDAS E INVALIDAS
# ==============================================================
def mostrar_operacion(numero, detalle):
    print("\nOPERACION " + str(numero) + ": " + detalle)


def ejecutar_simulacion():
    sistema = SistemaSoftwareFJ()

    mostrar_operacion(1, "Registrar cliente valido")
    ana = sistema.registrar_cliente("Ana Perez", "101234", "ana@correo.com")

    mostrar_operacion(2, "Registrar segundo cliente valido")
    luis = sistema.registrar_cliente("Luis Gomez", "105678", "luis@correo.com")

    mostrar_operacion(3, "Rechazar cliente sin nombre")
    sistema.registrar_cliente("", "109999", "persona@correo.com")

    mostrar_operacion(4, "Rechazar correo invalido")
    sistema.registrar_cliente("Marta Ruiz", "108888", "correo-invalido")

    mostrar_operacion(5, "Rechazar identificacion repetida")
    sistema.registrar_cliente("Otro cliente", "101234", "otro@correo.com")

    mostrar_operacion(6, "Crear servicio de sala")
    sala = sistema.crear_servicio("sala", "Sala de reuniones", 40000, 10)

    mostrar_operacion(7, "Crear servicio de alquiler de equipos")
    equipo = sistema.crear_servicio("equipo", "Computador portatil", 20000, 2)

    mostrar_operacion(8, "Crear servicio de asesoria")
    asesoria = sistema.crear_servicio("asesoria", "Asesoria tecnologica", 60000, "Software")

    mostrar_operacion(9, "Rechazar sala sin capacidad valida")
    sistema.crear_servicio("sala", "Sala incorrecta", 40000, 0)

    mostrar_operacion(10, "Rechazar equipo con tarifa negativa")
    sistema.crear_servicio("equipo", "Equipo incorrecto", -100, 1)

    mostrar_operacion(11, "Reserva valida de sala: sin ajustes")
    reserva_sala = sistema.realizar_reserva(ana, sala, 2)

    mostrar_operacion(12, "Reserva valida de equipos: descuento opcional")
    sistema.realizar_reserva(luis, equipo, 3, 10)

    mostrar_operacion(13, "Reserva valida de asesoria: descuento e impuesto")
    sistema.realizar_reserva(ana, asesoria, 1, 5, 19)

    mostrar_operacion(14, "Reserva invalida: duracion escrita con letras")
    sistema.realizar_reserva(ana, sala, "dos")

    mostrar_operacion(15, "Reserva fallida: servicio no disponible")
    sala.cambiar_disponibilidad(False)
    sistema.realizar_reserva(luis, sala, 1)

    mostrar_operacion(16, "Cancelar una reserva confirmada")
    sistema.cancelar_reserva(reserva_sala)

    mostrar_operacion(17, "Rechazar la cancelacion repetida")
    sistema.cancelar_reserva(reserva_sala)

    mostrar_operacion(18, "Confirmar que el programa sigue funcionando")
    sistema.realizar_reserva(luis, asesoria, 2)

    sistema.mostrar_resumen()
    print("\nRevise tambien el archivo: registro_software_fj.txt")


if __name__ == "__main__":
    ejecutar_simulacion()
