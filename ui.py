import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING


class CenterWidgetMixin:
    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class ClientWindowBase(Toplevel, CenterWidgetMixin):
    def __init__(self, parent, title, button_text, command, validate_indices=None, editable_dni=False):
        super().__init__(parent)
        self.title(title)
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()
        self.command = command
        self.validate_indices = validate_indices
        self.editable_dni = editable_dni

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        labels = ["DNI:", "Nombre (de 2 a 30 caracteres):", "Apellido (de 2 a 30 caracteres):"]
        entries = [Entry(frame) for _ in range(3)]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            Label(frame, text=label).grid(row=0, column=i)
            entry.grid(row=1, column=i)
            if i == 1 or i == 2:
                entry.bind("<KeyRelease>", lambda event, index=i-1: self.validate(event, index))
            elif i == 0 and not self.editable_dni:
                entry.config(state=DISABLED)

        frame_buttons = Frame(self)
        frame_buttons.pack(pady=10)

        button = Button(frame_buttons, text=button_text, command=self.command, state=DISABLED)
        button.grid(row=0, column=0)
        Button(frame_buttons, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [0, 0, 0]
        self.button = button
        self.entries = entries

    def command(self):
        pass

    def close(self):
        self.destroy()

    def validate(self, event, index):
        valor = event.widget.get()
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 \
            else (valor.isalpha() and 2 <= len(valor) <= 30)
        event.widget.config(bg="green" if valido else "red")
        self.validaciones[index] = valido
        self.button.config(state=NORMAL if all(self.validaciones) else DISABLED)


class CreateClientWindow(ClientWindowBase):
    def __init__(self, parent):
        super().__init__(
            parent,
            "Crear cliente",
            "Crear",
            self.create_client,
            validate_indices=[0, 1, 2],
            editable_dni=True
        )

    def create_client(self):
        self.master.treeview.insert(
            parent='',
            index='end',
            iid=self.entries[0].get(),
            values=(entry.get() for entry in self.entries)
        )
        db.Clientes.crear(self.entries[0].get(), self.entries[1].get(), self.entries[2].get())
        self.close()


class EditClientWindow(ClientWindowBase):
    def __init__(self, parent):
        super().__init__(
            parent,
            "Actualizar cliente",
            "Actualizar",
            self.edit_client,
            validate_indices=[1, 2],
            editable_dni=False
        )
        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, "values")
        self.entries[0].insert(0, campos[0])
        self.entries[1].insert(0, campos[1])
        self.entries[2].insert(0, campos[2])

    def edit_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(
            cliente,
            values=(entry.get() for entry in self.entries)
        )
        db.Clientes.modificar(self.entries[0].get(), self.entries[1].get(), self.entries[2].get())
        self.close()


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes")
        self.build()

    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview["columns"] = ("DNI", "Nombre", "Apellido")

        self.setup_treeview_columns(treeview)
        self.setup_treeview_heading(treeview)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview['yscrollcommand'] = scrollbar.set

        self.populate_treeview(treeview)

        treeview.pack()

        frame_buttons = Frame(self)
        frame_buttons.pack(pady=20)

        Button(frame_buttons, text="Crear", command=self.create).grid(row=0, column=0)
        Button(frame_buttons, text="Modificar", command=self.edit).grid(row=0, column=1)
        Button(frame_buttons, text="Borrar", command=self.delete).grid(row=0, column=2)

        self.treeview = treeview
        self.center()

    def setup_treeview_columns(self, treeview):
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

    def setup_treeview_heading(self, treeview):
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

    def populate_treeview(self, treeview):
        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='',
                index='end',
                iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel(
                title="Confirmar borrado",
                message=f"¿Está seguro que desea borrar a {campos[1]} {campos[2]}?",
                icon=WARNING
            )
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])

    def create(self):
        CreateClientWindow(self)

    def edit(self):
        cliente = self.treeview.focus()
        if cliente:
            EditClientWindow(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
