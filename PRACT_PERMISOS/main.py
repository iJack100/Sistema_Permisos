"""
=====================================================
  SISTEMA DE GESTIÓN DE PERMISOS DEL PERSONAL
=====================================================
Punto de entrada de la aplicación.
Ejecutar desde la raíz del proyecto:
    python main.py
"""

import sys
import os

# Asegurar que Python encuentre los módulos desde la raíz del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from views.menu_principal import MenuPrincipal


def main():
    app = MenuPrincipal()
    app.ejecutar()


if __name__ == "__main__":
    main()
