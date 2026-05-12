"""Formulario para consultar datos de empleados y tareas.

Permite buscar empleados por ID, ver sus tareas y consultar detalles.
"""

import tkinter as tk
from tkinter import messagebox
from views.base_form import BaseForm


class LookupForm(BaseForm):
    """Formulario para consultar datos de empleados y tareas.

    Permite buscar un empleado por ID, ver sus tareas y consultar
    detalles de tareas individuales.

    Attributes:
        controller (TaskController): Instancia del controlador.
        validator (module): Módulo con funciones de validación.

    Example:
        >>> form = LookupForm(master=root, controller=controller, validator=validaciones)
    """

    def __init__(self, master, controller, validator):
        """Inicializa el formulario de búsqueda.

        Args:
            master (tk.Widget): Ventana padre.
            controller (TaskController): Instancia del controlador.
            validator (module): Módulo con funciones de validación.
        """
        super().__init__(master=master, title="Lookup Employee / Task")
        self.controller = controller
        self.validator = validator
        self._build()

    def _build(self):
        """Construye los widgets del formulario."""
        tk.Label(self, text="Employee ID:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.emp_id_var = tk.StringVar()
        tk.Entry(self, textvariable=self.emp_id_var, width=8).grid(row=0, column=1, padx=6, pady=6, sticky="w")
        tk.Button(self, text="Load Employee", command=self.load_employee).grid(row=0, column=2, padx=6, pady=6)

        tk.Label(self, text="Employee:").grid(row=1, column=0, padx=6, pady=6, sticky="ne")
        self.emp_info_var = tk.StringVar(value="(not loaded)")
        tk.Label(self, textvariable=self.emp_info_var, justify="left").grid(row=1, column=1, columnspan=2, sticky="w")

        tk.Label(self, text="Tasks:").grid(row=2, column=0, padx=6, pady=6, sticky="ne")
        self.tasks_list = tk.Listbox(self, width=60, height=6)
        self.tasks_list.grid(row=2, column=1, columnspan=2, padx=6, pady=6, sticky="w")
        self.tasks_list.bind("<<ListboxSelect>>", self.on_task_select)

        tk.Label(self, text="Task ID:").grid(row=3, column=0, padx=6, pady=6, sticky="e")
        self.task_id_var = tk.StringVar()
        tk.Entry(self, textvariable=self.task_id_var, width=8).grid(row=3, column=1, padx=6, pady=6, sticky="w")
        tk.Button(self, text="Load Task", command=self.load_task_by_entry).grid(row=3, column=2, padx=6, pady=6)

        tk.Label(self, text="Task details:").grid(row=4, column=0, padx=6, pady=6, sticky="ne")
        self.task_info_var = tk.StringVar(value="(not loaded)")
        tk.Label(self, textvariable=self.task_info_var, justify="left").grid(row=4, column=1, columnspan=2, sticky="w")

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=8)
        tk.Button(btn_frame, text="Close", command=self.destroy).pack()

    def load_employee(self):
        """Carga datos del empleado por ID."""
        emp_text = self.emp_id_var.get().strip()
        if not self.validator.validate_int(emp_text):
            messagebox.showerror("Invalid input", "Employee ID must be an integer.")
            return
        emp_id = int(emp_text)
        try:
            emp = self.controller.lookup_employee(emp_id)
            self.emp_info_var.set(f"{emp[1]} <{emp[2] if emp[2] else ''}>")
            self.tasks_list.delete(0, tk.END)
            for t in self.controller.get_tasks(emp_id):
                self.tasks_list.insert(tk.END, f"{t['task_id']}: [{t['status']}] {t['description']}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_task_select(self, event):
        """Maneja selección de tarea en la lista."""
        sel = self.tasks_list.curselection()
        if not sel:
            return
        item = self.tasks_list.get(sel[0])
        task_id = int(item.split(":", 1)[0])
        self.load_task_by_id(task_id)

    def load_task_by_entry(self):
        """Carga tarea desde el campo de entrada."""
        tid_text = self.task_id_var.get().strip()
        if not self.validator.validate_int(tid_text):
            messagebox.showerror("Invalid input", "Task ID must be an integer.")
            return
        self.load_task_by_id(int(tid_text))

    def load_task_by_id(self, tid):
        """Carga y muestra detalles de una tarea."""
        try:
            task, emp_name = self.controller.lookup_task(tid)
            start = task[4] or "(none)"
            finish = task[5] or "(none)"
            self.task_info_var.set(
                f"Task {task[0]} for {emp_name}\n{task[2]} [{task[3]}]\nstart: {start}\nfinish: {finish}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
