from controllers.empleado_controller import EmpleadoController
from controllers.tipo_permiso_controller import TipoPermisoController
from controllers.permiso_controller import PermisoController
from controllers.stats_controller import StatsController
from core.decoradores import Color, Pantalla


class MenuPrincipal:
    """
    Vista principal del sistema. Orquesta todos los controladores
    y presenta el menú de navegación al usuario con colores y pantalla limpia.
    """

    def __init__(self):
        self._emp   = EmpleadoController()
        self._tp    = TipoPermisoController()
        self._per   = PermisoController(self._emp, self._tp)
        self._stats = StatsController(self._emp, self._tp, self._per)

    # ------------------------------------------------------------------
    # Helpers de presentación
    # ------------------------------------------------------------------
    def _imprimir_menu(self, titulo: str, opciones: list[tuple]):
        """Dibuja un submenú con colores usando Pantalla y Color."""
        Pantalla.encabezado(titulo)
        for clave, etiqueta in opciones:
            if clave == "0":
                print(Color.texto(f"  {clave}. {etiqueta}", Color.ROJO))
            else:
                print(Color.texto(f"  {clave}. ", Color.AMARILLO) + etiqueta)
        print(Pantalla.linea())
        return input(Color.texto("  Seleccione: ", Color.CYAN)).strip()

    # ------------------------------------------------------------------
    # Submenú: Registrar
    # ------------------------------------------------------------------
    def _menu_registrar(self):
        opciones = {
            "1": ("Registrar Empleado",        self._emp.crear),
            "2": ("Registrar Tipo de Permiso", self._tp.crear),
            "3": ("Registrar Permiso",         self._per.crear),
        }
        self._ejecutar_submenu("REGISTRAR", opciones)

    # ------------------------------------------------------------------
    # Submenú: Consultar
    # ------------------------------------------------------------------
    def _menu_consultar(self):
        opciones = {
            "1": ("Empleados",        self._emp.consultar),
            "2": ("Tipos de Permiso", self._tp.consultar),
            "3": ("Permisos",         self._per.consultar),
        }
        self._ejecutar_submenu("CONSULTAR", opciones)


    # ------------------------------------------------------------------
    # Submenú: Buscar
    # ------------------------------------------------------------------
    def _menu_buscar(self):
        opciones = {
            "1": ("Buscar Empleado",        lambda: self._emp.buscar()),
            "2": ("Buscar Tipo de Permiso", lambda: self._tp.buscar()),
            "3": ("Buscar Permiso",         lambda: self._per.buscar()),
        }
        self._ejecutar_submenu("BUSCAR", opciones)

    # ------------------------------------------------------------------
    # Submenú: Actualizar
    # ------------------------------------------------------------------
    def _menu_actualizar(self):
        opciones = {
            "1": ("Actualizar Empleado",        lambda: self._emp.actualizar()),
            "2": ("Actualizar Tipo de Permiso", lambda: self._tp.actualizar()),
            "3": ("Actualizar Permiso",         lambda: self._per.actualizar()),
        }
        self._ejecutar_submenu("ACTUALIZAR", opciones)

    # ------------------------------------------------------------------
    # Submenú: Eliminar
    # ------------------------------------------------------------------
    def _menu_eliminar(self):
        Pantalla.encabezado("ELIMINAR REGISTRO")
        print(Color.texto("  1. ", Color.AMARILLO) + "Eliminar Empleado")
        print(Color.texto("  2. ", Color.AMARILLO) + "Eliminar Tipo de Permiso")
        print(Color.texto("  3. ", Color.AMARILLO) + "Eliminar Permiso")
        print(Color.texto("  0. ", Color.ROJO)     + "Volver")
        print(Pantalla.linea())
        opc = input(Color.texto("  Seleccione: ", Color.CYAN)).strip()

        if opc == "1":
            emp_id = self._emp.eliminar()
            if emp_id:
                vinculados = len(list(filter(
                    lambda p: p.id_empleado == emp_id,
                    self._per.todos()
                )))
                if vinculados:
                    print(Color.texto(
                        f"  ⚠  Se eliminarán {vinculados} permiso(s) vinculado(s).",
                        Color.AMARILLO))
                    if input(Color.texto("  ¿Continuar? (1. Sí / 2. No): ", Color.ROJO)).strip() == "1":
                        self._per.eliminar_por_empleado(emp_id)
                        self._emp.eliminar_por_id(emp_id)
                        print(Color.texto("  ✔  Empleado y permisos eliminados.", Color.VERDE))
        elif opc == "2":
            tp_id = self._tp.eliminar()
            if tp_id:
                vinculados = len(list(filter(
                    lambda p: p.id_tipo_permiso == tp_id,
                    self._per.todos()
                )))
                if vinculados:
                    print(Color.texto(
                        f"  ⚠  Se eliminarán {vinculados} permiso(s) vinculado(s).",
                        Color.AMARILLO))
                    if input(Color.texto("  ¿Continuar? (1. Sí / 2. No): ", Color.ROJO)).strip() == "1":
                        self._per.eliminar_por_tipo(tp_id)
                        self._tp.eliminar_por_id(tp_id)
                        print(Color.texto("  ✔  Tipo de permiso y permisos eliminados.", Color.VERDE))
        elif opc == "3":
            self._per.eliminar()
        elif opc == "0":
            return
        else:
            print(Color.texto("  ⚠  Opción no válida.", Color.ROJO))

    # ------------------------------------------------------------------
    # Utilidad genérica de submenú
    # ------------------------------------------------------------------
    def _ejecutar_submenu(self, titulo: str, opciones: dict):
        while True:
            Pantalla.encabezado(titulo)
            for k, (label, _) in opciones.items():
                print(Color.texto(f"  {k}. ", Color.AMARILLO) + label)
            print(Color.texto("  0. ", Color.ROJO) + "Volver")
            print(Pantalla.linea())
            opc = input(Color.texto("  Seleccione: ", Color.CYAN)).strip()
            if opc == "0":
                break
            elif opc in opciones:
                opciones[opc][1]()
            else:
                print(Color.texto("  ⚠  Opción no válida.", Color.ROJO))
                Pantalla.pausar()

    # ------------------------------------------------------------------
    # Bucle principal
    # ------------------------------------------------------------------
    def ejecutar(self):
        while True:
            Pantalla.encabezado("SISTEMA DE GESTIÓN DE PERMISOS DEL PERSONAL")

            # Posicionar opciones con gotoxy
            Pantalla.gotoxy(2, 6)
            print(Color.texto("  1. ", Color.AMARILLO) + "Registrar")
            Pantalla.gotoxy(2, 7)
            print(Color.texto("  2. ", Color.AMARILLO) + "Consultar")
            Pantalla.gotoxy(2, 8)
            print(Color.texto("  3. ", Color.AMARILLO) + "Buscar")
            Pantalla.gotoxy(2, 9)
            print(Color.texto("  4. ", Color.AMARILLO) + "Actualizar")
            Pantalla.gotoxy(2, 10)
            print(Color.texto("  5. ", Color.AMARILLO) + "Eliminar")
            Pantalla.gotoxy(2, 11)
            print(Color.texto("  6. ", Color.AMARILLO) + "Estadísticas de Permisos")
            Pantalla.gotoxy(2, 12)
            print(Color.texto("  7. ", Color.AMARILLO) + "Resumen General")
            Pantalla.gotoxy(2, 13)
            print(Color.texto("  0. ", Color.ROJO)     + "Salir")
            Pantalla.gotoxy(2, 14)
            print(Pantalla.linea())
            Pantalla.gotoxy(2, 15)
            opc = input(Color.texto("  Seleccione una opción: ", Color.CYAN)).strip()

            if   opc == "1": self._menu_registrar()
            elif opc == "2": self._menu_consultar()
            elif opc == "3": self._menu_buscar()
            elif opc == "4": self._menu_actualizar()
            elif opc == "5": self._menu_eliminar()
            elif opc == "6": self._per.estadisticas()
            elif opc == "7": self._stats.resumen_general()
            elif opc == "0":
                Pantalla.limpiar()
                print(Color.texto("\n  Hasta luego. ¡Que tenga un buen día!\n", Color.VERDE))
                break
            else:
                print(Color.texto("  ⚠  Opción no válida.", Color.ROJO))
                Pantalla.pausar()
