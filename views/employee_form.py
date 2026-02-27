"""Formulario para agregar empleados.

Permite ingresar nombre, apellido, país y email del empleado.
"""

import tkinter as tk
from tkinter import messagebox
from views.base_form import BaseForm


class EmployeeForm(BaseForm):
    """Formulario para agregar un nuevo empleado.

    Permite ingresar nombre, apellido, país y email del empleado.
    Valida los datos antes de enviarlos al controlador.

    Attributes:
        submit_callback (callable): Función a ejecutar al enviar el formulario.
        validator (module): Módulo con funciones de validación.

    Example:
        >>> def on_submit(name, surname, country, email):
        ...     print(f"Empleado: {name} {surname}")
        ...
        >>> form = EmployeeForm(master=root, submit_callback=on_submit, validator=validaciones)
    """

    def __init__(self, master, submit_callback, validator):
        """Inicializa el formulario de empleado.

        Args:
            master (tk.Widget): Ventana padre.
            submit_callback (callable): Función a ejecutar al enviar el formulario.
            validator (module): Módulo con funciones de validación.
        """
        super().__init__(master=master, title="Add Employee")
        self.submit_callback = submit_callback
        self.validator = validator
        self._build()

    def _build(self):
        """Construye los widgets del formulario."""
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=6, pady=6)

        tk.Label(self, text="Surname:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        self.surname_var = tk.StringVar()
        tk.Entry(self, textvariable=self.surname_var, width=30).grid(row=1, column=1, padx=6, pady=6)

        tk.Label(self, text="Country:").grid(row=2, column=0, padx=6, pady=6, sticky="e")
        self.country_var = tk.StringVar()
        tk.Entry(self, textvariable=self.country_var, width=30).grid(row=2, column=1, padx=6, pady=6)

        tk.Label(self, text="Email:").grid(row=3, column=0, padx=6, pady=6, sticky="e")
        self.email_var = tk.StringVar()
        tk.Entry(self, textvariable=self.email_var, width=30).grid(row=3, column=1, padx=6, pady=6)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Submit", command=self._on_submit).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancel", command=self._on_cancel).pack(side="left", padx=6)

    def _on_submit(self):
        """Valida y envía los datos del formulario."""
        name = self.name_var.get().strip()
        surname = self.surname_var.get().strip()
        country = self.country_var.get().strip()
        email = self.email_var.get().strip()

        if not self.validator.validate_nonempty(name):
            messagebox.showerror("Invalid input", "Name cannot be empty.")
            return
        if not self.validator.validate_email(email):
            messagebox.showerror("Invalid input", "Email looks invalid.")
            return
        try:
            msg = self.submit_callback(name, surname, country, email)
            messagebox.showinfo("Success", msg)
            self.destroy()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _on_cancel(self):
        """Cierra el formulario sin enviar."""
        self.destroy()
