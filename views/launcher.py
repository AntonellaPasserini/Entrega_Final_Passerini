"""Ventana principal de la aplicación.

Orquesta la interfaz principal con dos Treeviews (Empleados y Tareas)
y botones para realizar operaciones CRUD.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class Launcher(tk.Tk):
    """Ventana principal de la aplicación.

    Muestra un Treeview para empleados y otro para tareas. Permite
    agregar, eliminar, buscar y consultar registros.

    Attributes:
        controller (TaskController): Instancia del controlador.
        validator (module): Módulo con funciones de validación.
        ui_manager (UIManager): Gestor de UI.

    Example:
        >>> app = Launcher(controller=controller, validator=validaciones, ui_manager=ui_mgr)
        >>> app.mainloop()
    """

    def __init__(self, controller, validator, ui_manager):
        """Inicializa la ventana principal.

        Args:
            controller (TaskController): Instancia del controlador.
            validator (module): Módulo con funciones de validación.
            ui_manager (UIManager): Gestor de UI.
        """
        super().__init__()
        self.title("Task DB Application")
        self.geometry("900x600")
        self.controller = controller
        self.validator = validator
        self.ui_manager = ui_manager

        self._build()
        self.refresh_employee_tree()

    def _build(self):
        """Construye la interfaz principal."""
        # Frame superior para botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=6, pady=6)

        tk.Button(btn_frame, text="Add Employee", command=self.on_add_employee).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Add Task", command=self.on_add_task).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Lookup", command=self.on_lookup).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Delete Employee", command=self.on_delete_employee).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Refresh", command=self.on_refresh).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Exit", command=self.quit).pack(side=tk.LEFT, padx=3)

        # Panframe para Treeviews
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Treeview Empleados
        emp_frame = tk.Frame(paned)
        paned.add(emp_frame, weight=1)
        tk.Label(emp_frame, text="Employees:", font=("Arial", 10, "bold")).pack(anchor="w")
       
        self.emp_tree = ttk.Treeview(emp_frame, columns=("name", "email", "country"), height=12)
        self.emp_tree.column("#0", width=60, anchor="center")  # ID column
        self.emp_tree.column("name", width=140, anchor="w")
        self.emp_tree.column("email", width=150, anchor="w")
        self.emp_tree.column("country", width=80, anchor="w")
        self.emp_tree.heading("#0", text="ID")
        self.emp_tree.heading("name", text="Name")
        self.emp_tree.heading("email", text="Email")
        self.emp_tree.heading("country", text="Country")
        self.emp_tree.pack(fill=tk.BOTH, expand=True)

        # Treeview Tareas
        task_frame = tk.Frame(paned)
        paned.add(task_frame, weight=1)
        tk.Label(task_frame, text="Tasks:", font=("Arial", 10, "bold")).pack(anchor="w")
       
        self.task_tree = ttk.Treeview(task_frame, columns=("description", "employee", "status"), height=12)
        self.task_tree.column("#0", width=60, anchor="center")  # ID column
        self.task_tree.column("description", width=200, anchor="w")
        self.task_tree.column("employee", width=100, anchor="w")
        self.task_tree.column("status", width=80, anchor="w")
        self.task_tree.heading("#0", text="ID")
        self.task_tree.heading("description", text="Description")
        self.task_tree.heading("employee", text="Employee")
        self.task_tree.heading("status", text="Status")
        self.task_tree.pack(fill=tk.BOTH, expand=True)

    def on_add_employee(self):
        """Abre formulario para agregar empleado."""
        self.ui_manager.open_employee_form(callback=self.on_employee_added)

    def on_add_task(self):
        """Abre formulario para agregar tarea."""
        self.ui_manager.open_task_form(callback=self.on_task_added)

    def on_lookup(self):
        """Abre formulario de búsqueda."""
        self.ui_manager.open_lookup_form()

    def on_delete_employee(self):
        """Abre formulario de eliminación de empleado."""
        self.ui_manager.open_delete_employee_form(callback=self.on_employee_deleted)

    def on_refresh(self):
        """Refresca ambos Treeviews."""
        self.refresh_employee_tree()
        self.refresh_task_tree()

    def on_employee_added(self, *args):
        """Callback para cuando se agrega un empleado."""
        self.refresh_employee_tree()

    def on_task_added(self, *args):
        """Callback para cuando se agrega una tarea."""
        self.refresh_task_tree()
        self.refresh_employee_tree()

    def on_employee_deleted(self, *args):
        """Callback para cuando se elimina un empleado."""
        self.refresh_employee_tree()
        self.refresh_task_tree()

    def refresh_employee_tree(self):
        """Recarga la lista de empleados en el Treeview."""
        # Borra contenido anterior
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)

        try:
            employees = self.controller.get_all_employees()
            for emp_id, name, surname, email, country in employees:
                full_name = f"{name} {surname}"
                # Put emp_id in the tree (#0) so ID appears as the first column
                self.emp_tree.insert("", "end", text=str(emp_id), values=(full_name, email, country))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load employees: {e}")

    def refresh_task_tree(self):
        """Recarga la lista de tareas en el Treeview."""
        # Borra contenido anterior
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        try:
            tasks = self.controller.get_all_tasks_combined()
            for task_id, desc, status, emp_name in tasks:
                # Put task_id in the tree (#0) so ID appears as the first column
                self.task_tree.insert("", "end", text=str(task_id), values=(desc, emp_name, status))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load tasks: {e}")
