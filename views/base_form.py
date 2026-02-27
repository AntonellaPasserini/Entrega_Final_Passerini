"""Clase base para formularios emergentes.

Proporciona funcionalidad común para todos los formularios.
"""

import tkinter as tk
from typing import Callable


class BaseForm(tk.Toplevel):
    """Clase base para formularios emergentes.

    Proporciona funcionalidad común para todos los formularios como
    manejo de cierre de ventana y callback al destruirse.

    Attributes:
        on_close (callable, optional): Función a ejecutar al cerrar la ventana.

    Example:
        >>> class MyForm(BaseForm):
        ...     def _build(self):
        ...         tk.Label(self, text="Content").pack()
        ...
        >>> form = MyForm(master=root, title="My Form")
    """

    def __init__(self, master=None, title: str = "", on_close: Callable | None = None):
        """Inicializa un formulario emergente.

        Args:
            master (tk.Widget, optional): Ventana padre.
            title (str, optional): Título de la ventana.
            on_close (callable, optional): Función a ejecutar al cerrar.
        """
        super().__init__(master=master)
        self.title(title)
        self.on_close = on_close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        """Ejecuta callback al cerrar y destruye la ventana."""
        if self.on_close:
            self.on_close()
        self.destroy()

    def _build(self):
        """Construye la interfaz del formulario.

        Debe ser implementado por subclases para crear sus widgets.
        """
        raise NotImplementedError("Subclasses must implement _build()")
