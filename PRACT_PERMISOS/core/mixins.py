import re
from datetime import datetime


class CalculosMixin:
    """
    Mixin con validaciones robustas y cálculos reutilizables.
    Todos los métodos pedir_* hacen el input + validación en un bucle
    hasta que el usuario ingrese un valor correcto.
    """

    # ══════════════════════════════════════════
    # CÁLCULOS
    # ══════════════════════════════════════════

    def validar_fecha(self, fecha_str: str):
        """Convierte 'DD/MM/YYYY' a datetime. Retorna None si es inválida."""
        try:
            return datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            return None

    def calcular_descuento(self, tipo: str, tiempo: float, valor_hora: float, remunerado: str) -> float:
        if remunerado == "S":
            return 0.0
        factor = 8 if tipo == "D" else 1
        return round(float(tiempo) * factor * valor_hora, 2)

    def formatear_moneda(self, valor: float) -> str:
        return f"$ {valor:,.2f}"

    # ══════════════════════════════════════════
    # VALIDACIONES ESTÁTICAS (retornan o lanzan ValueError)
    # ══════════════════════════════════════════

    @staticmethod
    def validar_no_vacio(valor: str, campo: str) -> str:
        """Valida que no esté vacío."""
        v = valor.strip()
        if not v:
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        return v

    @staticmethod
    def validar_solo_letras(valor: str, campo: str) -> str:
        """Valida que solo contenga letras y espacios (sin números ni símbolos)."""
        v = valor.strip()
        if not v:
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        if not re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+", v):
            raise ValueError(f"'{campo}' solo puede contener letras y espacios, sin números ni símbolos.")
        return v

    @staticmethod
    def validar_texto_general(valor: str, campo: str, min_len: int = 3) -> str:
        """Valida texto libre: no vacío, sin números puros, longitud mínima."""
        v = valor.strip()
        if not v:
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        if len(v) < min_len:
            raise ValueError(f"'{campo}' debe tener al menos {min_len} caracteres.")
        if v.isdigit():
            raise ValueError(f"'{campo}' no puede ser solo números.")
        return v

    @staticmethod
    def validar_entero_positivo(valor: str, campo: str) -> int:
        """Valida que sea un entero positivo."""
        v = valor.strip()
        if not v.isdigit():
            raise ValueError(f"'{campo}' debe ser un número entero positivo (sin decimales ni letras).")
        n = int(v)
        if n <= 0:
            raise ValueError(f"'{campo}' debe ser mayor a 0.")
        return n

    @staticmethod
    def validar_positivo(valor: str, campo: str) -> float:
        """Valida que sea un número decimal positivo."""
        v = valor.strip().replace(",", ".")
        try:
            n = float(v)
        except ValueError:
            raise ValueError(f"'{campo}' debe ser un número válido (ej: 1200.50).")
        if n <= 0:
            raise ValueError(f"'{campo}' debe ser mayor a 0.")
        return n

    @staticmethod
    def validar_si_no(valor: str) -> str:
        v = valor.strip().upper()
        if v not in ("S", "N"):
            raise ValueError("Respuesta debe ser 'S' o 'N'.")
        return v

    @staticmethod
    def validar_tipo_permiso(valor: str) -> str:
        v = valor.strip().upper()
        if v not in ("D", "H"):
            raise ValueError("Tipo debe ser 'D' (días) o 'H' (horas).")
        return v

    @staticmethod
    def validar_opcion_menu(valor: str, opciones_validas: tuple) -> str:
        v = valor.strip()
        if v not in opciones_validas:
            raise ValueError(f"Opción inválida. Ingrese una de: {', '.join(opciones_validas)}")
        return v

    # ══════════════════════════════════════════
    # INPUTS CON REINTENTO (bucle hasta valor válido)
    # ══════════════════════════════════════════

    @staticmethod
    def _pedir(prompt: str, validador, color_prompt=None, color_error=None) -> object:
        """
        Método base: muestra el prompt, llama al validador y repite
        hasta obtener un valor válido. Importa Color aquí para evitar
        dependencia circular en el módulo.
        """
        from core.decoradores import Color
        cp = color_prompt or Color.BLANCO
        ce = color_error  or Color.ROJO
        while True:
            try:
                raw = input(f"{cp}{prompt}{Color.RESET}")
                return validador(raw)
            except (ValueError, TypeError) as e:
                print(Color.texto(f"  ⚠  {e}", ce))

    @classmethod
    def pedir_nombre(cls, prompt: str = "  Nombre       : ") -> str:
        """Pide un nombre: solo letras y espacios, no vacío."""
        return cls._pedir(prompt, lambda v: cls.validar_solo_letras(v, "nombre"))

    @classmethod
    def pedir_descripcion(cls, prompt: str = "  Descripción  : ") -> str:
        """Pide una descripción: texto general, mínimo 3 caracteres."""
        return cls._pedir(prompt, lambda v: cls.validar_texto_general(v, "descripción"))

    @classmethod
    def pedir_sueldo(cls, prompt: str = "  Sueldo       : ") -> float:
        """Pide un sueldo: decimal positivo."""
        return cls._pedir(prompt, lambda v: cls.validar_positivo(v, "sueldo"))

    @classmethod
    def pedir_entero(cls, prompt: str, campo: str = "valor") -> int:
        """Pide un entero positivo."""
        return cls._pedir(prompt, lambda v: cls.validar_entero_positivo(v, campo))

    @classmethod
    def pedir_decimal(cls, prompt: str, campo: str = "valor") -> float:
        """Pide un decimal positivo."""
        return cls._pedir(prompt, lambda v: cls.validar_positivo(v, campo))

    @classmethod
    def pedir_si_no(cls, prompt: str) -> str:
        """Pide S o N, repite hasta obtener respuesta válida."""
        return cls._pedir(prompt, lambda v: cls.validar_si_no(v))

    @classmethod
    def pedir_tipo_permiso(cls, prompt: str = "  Tipo (D/H)   : ") -> str:
        """Pide D o H, repite hasta obtener respuesta válida."""
        return cls._pedir(prompt, lambda v: cls.validar_tipo_permiso(v))

    @classmethod
    def pedir_fecha(cls, prompt: str) -> tuple:
        """
        Pide una fecha en formato DD/MM/YYYY.
        Retorna (fecha_str, datetime_obj).
        """
        from core.decoradores import Color

        def _validar_fecha(raw: str):
            raw = raw.strip()
            if not raw:
                raise ValueError("La fecha no puede estar vacía.")
            # Verificar formato básico con regex
            if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", raw):
                raise ValueError("Formato inválido. Use DD/MM/YYYY (ej: 25/04/2025).")
            try:
                dt = datetime.strptime(raw, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Fecha inexistente (ej: 30/02/2025 no existe).")
            return (raw, dt)

        return cls._pedir(prompt, _validar_fecha)
