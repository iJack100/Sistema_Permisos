# Sistema de Gestión de Permisos del Personal

Aplicación de consola desarrollada en **Python puro** (sin frameworks) que gestiona el registro de empleados, tipos de permisos y solicitudes de permisos laborales, con cálculo automático de descuentos y persistencia en JSON.

---

## Estructura del proyecto

```
PRACT_PERMISOS/
│
├── main.py                        # Punto de entrada
│
├── core/                          # Núcleo del sistema
│   ├── interfaces.py              # Clase abstracta ICrud
│   ├── mixins.py                  # CalculosMixin (validaciones y cálculos)
│   ├── decoradores.py             # decorador_interfaz, manejar_errores
│   └── json_manager.py            # Lectura/escritura de archivos JSON
│
├── models/                        # Entidades del dominio
│   ├── empleado.py
│   ├── tipo_permiso.py
│   └── permiso.py
│
├── controllers/                   # Lógica CRUD por entidad
│   ├── empleado_controller.py
│   ├── tipo_permiso_controller.py
│   ├── permiso_controller.py      # Estadísticas con HOF
│   └── stats_controller.py
│
├── views/                         # Interfaz de usuario (consola)
│   └── menu_principal.py
│
├── data/                          # Persistencia JSON
│   ├── empleados.json
│   ├── tipos_permisos.json
│   └── permisos.json
│
└── docs/
    └── architecture.excalidraw    # Diagrama de arquitectura (opcional)
```

---

## Cómo ejecutar

```bash
# Desde la carpeta raíz del proyecto
python main.py
```

---

## Conceptos aplicados

| Concepto | Archivo(s) |
|---|---|
| Clases abstractas / Interfaces | `core/interfaces.py` |
| Mixins | `core/mixins.py` |
| Decoradores | `core/decoradores.py` |
| Funciones de orden superior (map, filter, reduce) | `controllers/permiso_controller.py`, `controllers/stats_controller.py` |
| Persistencia JSON | `core/json_manager.py` |
| POO (herencia múltiple) | Todos los controllers |

---

## Reglas de negocio

- El **valor hora** se calcula como `sueldo / 240`.
- Si el tipo de permiso es **remunerado (S)**, el descuento es `$0`.
- Si el tipo es **no remunerado (N)**:
  - Tipo **D** (días): `tiempo × 8 × valor_hora`
  - Tipo **H** (horas): `tiempo × valor_hora`
- Al eliminar un empleado o tipo de permiso, se eliminan en cascada los permisos vinculados.
