"""Formulario para eliminar empleados.

Permite eliminar un empleado con confirmación de tareas asociadas.
"""

import tkinter as tk
from tkinter import messagebox
from views.base_form import BaseForm


class DeleteEmployeeForm(BaseForm):
    """Formulario para eliminar empleados de la base de datos.

    Valida que el empleado exista, muestra sus tareas asociadas
    y pide confirmación antes de eliminar.

    Attributes:
        controller (TaskController): Instancia del controlador.
        validator (module): Módulo con funciones de validación.

    Example:
        >>> form = DeleteEmployeeForm(master=root, controller=controller, validator=validaciones)
    """

    def __init__(self, master, controller, validator):
        """Inicializa el formulario de eliminación de empleado.

        Args:
            master (tk.Widget): Ventana padre.
            controller (TaskController): Instancia del controlador.
            validator (module): Módulo con funciones de validación.
        """
        super().__init__(master=master, title="Delete Employee")
        self.controller = controller
        self.validator = validator
        self._build()

    def _build(self):
        """Construye los widgets del formulario."""
        tk.Label(self, text="Employee ID:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.emp_id_var = tk.StringVar()
        tk.Entry(self, textvariable=self.emp_id_var, width=8).grid(row=0, column=1, padx=6, pady=6, sticky="w")

        tk.Label(self, text="Employee:").grid(row=1, column=0, padx=6, pady=6, sticky="ne")
        self.emp_info_var = tk.StringVar(value="(not loaded)")
        tk.Label(self, textvariable=self.emp_info_var, justify="left").grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Tasks:").grid(row=2, column=0, padx=6, pady=6, sticky="ne")
        self.tasks_text = tk.Text(self, width=60, height=6)
        self.tasks_text.grid(row=2, column=1, padx=6, pady=6)
        self.tasks_text.config(state=tk.DISABLED)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Load Employee", command=self.load_employee).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Delete Employee", command=self.delete_employee).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=4)

    def load_employee(self):
        """Carga datos del empleado a eliminar."""
        emp_text = self.emp_id_var.get().strip()
        if not self.validator.validate_int(emp_text):
            messagebox.showerror("Invalid input", "Employee ID must be an integer.")
            return

        emp_id = int(emp_text)
        try:
            emp = self.controller.lookup_employee(emp_id)
            self.emp_info_var.set(f"{emp[1]} {emp[2]} <{emp[3] if emp[3] else ''}>")

            tasks = self.controller.get_tasks(emp_id)
            task_count = len(tasks)

            self.tasks_text.config(state=tk.NORMAL)
            self.tasks_text.delete(1.0, tk.END)
            if task_count == 0:
                self.tasks_text.insert(tk.END, "No tasks for this employee.")
            else:
                for t in tasks:
                    status = t['status']
                    desc = t['description']
                    self.tasks_text.insert(tk.END, f"- [{status}] {desc}\n")
            self.tasks_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_employee(self):
        """Elimina el empleado con confirmación."""
        emp_text = self.emp_id_var.get().strip()
        if not self.validator.validate_int(emp_text):
            messagebox.showerror("Invalid input", "Employee ID must be an integer.")
            return

        emp_id = int(emp_text)
        emp_info = self.emp_info_var.get()
        if emp_info == "(not loaded)":
            messagebox.showwarning("Not loaded", "Load employee first.")
            return

        # Pide confirmación
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete {emp_info}?\nAll associated tasks will also be deleted.",
        )
        if not result:
            return

        try:
            self.controller.delete_employee(emp_id)
            messagebox.showinfo("Success", f"Employee {emp_id} deleted successfully.")
            self._on_cancel()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_cancel(self):
        """Cierra el formulario."""
        self.master.destroy()
