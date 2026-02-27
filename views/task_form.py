"""Formulario para agregar tareas.

Permite seleccionar un empleado, escribir descripción y establecer estado.
"""

import tkinter as tk
from tkinter import messagebox
from views.base_form import BaseForm


class TaskForm(BaseForm):
    """Formulario para agregar una nueva tarea.

    Permite seleccionar un empleado, escribir descripción de la tarea
    y establecer su estado inicial.

    Attributes:
        submit_callback (callable): Función a ejecutar al enviar.
        validator (module): Módulo con funciones de validación.

    Example:
        >>> def on_submit(emp_id, description, status):
        ...     print(f"Tarea para {emp_id}: {description}")
        ...
        >>> form = TaskForm(master=root, submit_callback=on_submit, validator=validaciones)
    """

    def __init__(self, master, submit_callback, validator):
        """Inicializa el formulario de tarea.

        Args:
            master (tk.Widget): Ventana padre.
            submit_callback (callable): Función a ejecutar al enviar.
            validator (module): Módulo con funciones de validación.
        """
        super().__init__(master=master, title="Add Task")
        self.submit_callback = submit_callback
        self.validator = validator
        self._build()

    def _build(self):
        """Construye los widgets del formulario."""
        tk.Label(self, text="Employee ID:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.emp_var = tk.StringVar()
        tk.Entry(self, textvariable=self.emp_var, width=10).grid(row=0, column=1, padx=6, pady=6)

        tk.Label(self, text="Description:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        self.desc_var = tk.StringVar()
        tk.Entry(self, textvariable=self.desc_var, width=40).grid(row=1, column=1, padx=6, pady=6)

        tk.Label(self, text="Status:").grid(row=2, column=0, padx=6, pady=6, sticky="e")
        self.status_var = tk.StringVar(value="todo")
        tk.Entry(self, textvariable=self.status_var, width=15).grid(row=2, column=1, padx=6, pady=6, sticky="w")

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Submit", command=self._on_submit).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancel", command=self._on_cancel).pack(side="left", padx=6)

    def _on_submit(self):
        """Valida y envía los datos del formulario."""
        emp_text = self.emp_var.get().strip()
        desc = self.desc_var.get().strip()
        status = self.status_var.get().strip() or "todo"

        if not self.validator.validate_int(emp_text):
            messagebox.showerror("Invalid input", "Employee ID must be an integer.")
            return
        emp_id = int(emp_text)
        if not self.validator.validate_nonempty(desc):
            messagebox.showerror("Invalid input", "Description cannot be empty.")
            return
        try:
            msg = self.submit_callback(emp_id, desc, status)
            messagebox.showinfo("Success", msg)
            self.destroy()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _on_cancel(self):
        """Cierra el formulario sin enviar."""
        self.destroy()
