import os
import functools

# ─────────────────────────────────────────────
# COLORES ANSI
# ─────────────────────────────────────────────

class Color:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    ROJO     = "\033[31m"
    VERDE    = "\033[32m"
    AMARILLO = "\033[33m"
    AZUL     = "\033[34m"
    MAGENTA  = "\033[35m"
    CYAN     = "\033[36m"
    BLANCO   = "\033[37m"

    @staticmethod
    def texto(texto, color):
        return f"{color}{texto}{Color.RESET}"

    @staticmethod
    def titulo(texto, color=None):
        color = color or Color.CYAN
        return f"{Color.BOLD}{color}{texto}{Color.RESET}"


# ─────────────────────────────────────────────
# PANTALLA: limpiar, gotoxy, pausar
# ─────────────────────────────────────────────

class Pantalla:

    @staticmethod
    def limpiar():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def gotoxy(x, y):
        """Mueve el cursor a la posición (columna x, fila y)."""
        print(f"\033[{y};{x}H", end="", flush=True)

    @staticmethod
    def pausar():
        input(f"\n  {Color.texto('Presione ENTER para continuar...', Color.AMARILLO)}")

    @staticmethod
    def linea(caracter="─", ancho=50, color=None):
        return Color.texto(caracter * ancho, color or Color.AZUL)

    @staticmethod
    def encabezado(titulo, color=None):
        color = color or Color.CYAN
        ancho = 50
        Pantalla.limpiar()
        print(Color.texto("═" * ancho, color))
        print(Color.titulo(titulo.center(ancho), color))
        print(Color.texto("═" * ancho, color))


# ─────────────────────────────────────────────
# DECORADORES
# ─────────────────────────────────────────────

def decorador_interfaz(titulo: str):
    """
    Decorador de fábrica: limpia la pantalla y muestra un encabezado
    con el título dado antes de ejecutar la función decorada.
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            Pantalla.encabezado(titulo)
            return func(*args, **kwargs)
        return inner
    return wrapper


def manejar_errores(func):
    """
    Decorador que captura excepciones comunes y las muestra al usuario
    con colores de error, sin cortar la ejecución del programa.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(Color.texto(f"\n  ⚠  Error de valor: {e}", Color.ROJO))
        except FileNotFoundError as e:
            print(Color.texto(f"\n  ⚠  Error de archivo: {e}", Color.ROJO))
        except Exception as e:
            print(Color.texto(f"\n  ⚠  Error inesperado: {type(e).__name__} — {e}", Color.ROJO))
    return wrapper


# ─────────────────────────────────────────────
# DECORADOR: VALIDAR CÉDULA ECUATORIANA
# ─────────────────────────────────────────────

def validar_cedula(func):
    """
    Decorador que valida una cédula ecuatoriana antes de ejecutar
    la función decorada.

    ALGORITMO DE VALIDACIÓN:
      1. Debe tener exactamente 10 dígitos numéricos.
      2. Los dos primeros dígitos representan la provincia (01-24).
      3. Algoritmo Módulo 10 (dígito verificador):
         - Coeficientes: [2,1,2,1,2,1,2,1,2] sobre los 9 primeros dígitos.
         - Si el producto >= 10, restar 9.
         - Sumar todos los resultados.
         - Dígito esperado = (10 - (suma % 10)) % 10
         - Debe coincidir con el décimo dígito.

    USO:
        La función decorada debe recibir la cédula como kwarg 'cedula'
        o como segundo argumento posicional (self, cedula, ...).

        @validar_cedula
        def registrar(self, cedula, nombre):
            ...

    Si la cédula no es válida, imprime el error con color rojo
    y retorna None sin llamar a la función original.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Obtener la cédula: primero kwargs, luego args[1] (después de self)
        cedula = kwargs.get("cedula") or (args[1] if len(args) > 1 else None)

        if cedula is not None:
            cedula = str(cedula).strip()

            # Validación 1: exactamente 10 dígitos numéricos
            if not cedula.isdigit() or len(cedula) != 10:
                print(Color.texto(
                    "\n  ⚠  Cédula inválida: debe tener exactamente 10 dígitos numéricos.",
                    Color.ROJO))
                return None

            # Validación 2: código de provincia (01-24)
            provincia = int(cedula[:2])
            if provincia < 1 or provincia > 24:
                print(Color.texto(
                    f"\n  ⚠  Cédula inválida: provincia '{cedula[:2]}' no existe (rango 01-24).",
                    Color.ROJO))
                return None

            # Validación 3: algoritmo Módulo 10
            coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
            total = 0
            for i in range(9):
                val = int(cedula[i]) * coeficientes[i]
                if val >= 10:
                    val -= 9
                total += val

            digito_esperado = (10 - (total % 10)) % 10
            digito_real = int(cedula[9])

            if digito_esperado != digito_real:
                print(Color.texto(
                    f"\n  ⚠  Cédula inválida: dígito verificador incorrecto "
                    f"(esperado {digito_esperado}, recibido {digito_real}).",
                    Color.ROJO))
                return None

        # Ejecutar la función original si todo es válido
        return func(*args, **kwargs)

    return wrapper