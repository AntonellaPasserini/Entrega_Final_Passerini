"""Gestor centralizado de interfaz de usuario.

Orquesta la creación y ciclo de vida de todos los formularios y ventanas.
Implementa el patrón Facade para simplificar el acceso a componentes de UI.
"""

import tkinter as tk
from typing import Optional, Any
from views.employee_form import EmployeeForm
from views.task_form import TaskForm
from views.lookup_form import LookupForm
from views.delete_employee_form import DeleteEmployeeForm


class UIManager:
    """Gestor centralizado de interfaz de usuario.

    Orquesta la creación y destrucción de ventanas modales y principales.
    Centraliza el acceso a formularios, callbacks y operaciones de UI.

    Attributes:
        root (tk.Tk): Ventana raíz de la aplicación.
        controller (TaskController): Instancia del controlador.
        validator (module): Módulo con funciones de validación.

    Example:
        >>> ui_manager = UIManager(root=root, controller=controller, validator=validaciones)
        >>> ui_manager.open_employee_form(callback=on_employee_added)
    """

    def __init__(self, root: Optional[Any], controller, validator):
        """Inicializa el gestor de UI.

        Args:
            root (tk.Tk): Ventana raíz de la aplicación.
            controller (TaskController): Instancia del controlador.
            validator (module): Módulo con funciones de validación.
        """
        self.root:Optional[Any] = root
        self.controller = controller
        self.validator = validator

    def open_employee_form(self, callback=None):
        """Abre el formulario para agregar empleado.

        Args:
            callback (Callable | None): Función a ejecutar tras agregar empleado.
        """
        def on_submit(name, surname, country, email):
            msg = self.controller.add_employee(name, surname, country, email)
            if callback:
                callback()
            return msg

        form = EmployeeForm(master=self.root, submit_callback=on_submit, validator=self.validator)
        if self.root:
            self.root.wait_window(form)

    def open_task_form(self, callback=None):
        """Abre el formulario para agregar tarea.

        Args:
            callback (Callable | None): Función a ejecutar tras agregar tarea.
        """
        def on_submit(emp_id, description, status):
            msg = self.controller.add_task(emp_id, description, status)
            if callback:
                callback()
            return msg

        form = TaskForm(master=self.root, submit_callback=on_submit, validator=self.validator)
        if self.root:
            self.root.wait_window(form)

    def open_lookup_form(self):
        """Abre el formulario de búsqueda/consulta.

        Permite buscar empleados y tareas sin realizar cambios.
        """
        form = LookupForm(master=self.root, controller=self.controller, validator=self.validator)
        if self.root:
            self.root.wait_window(form)

    def open_delete_employee_form(self, callback=None):
        """Abre el formulario para eliminar empleado.

        Args:
            callback (Callable | None): Función a ejecutar tras eliminar empleado.
        """
        def on_delete():
            if callback:
                callback()

        form = DeleteEmployeeForm(master=self.root, controller=self.controller, validator=self.validator)
        if self.root:
            self.root.wait_window(form)
