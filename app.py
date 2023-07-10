""" Employee management system app using Python """
from tkinter import *  # type:ignore
from tkinter import messagebox, ttk
from conn_with_db import *


class Main:
    def __init__(self):
        self.root = Tk()
        self.win_width = self.root.winfo_screenwidth()
        self.win_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.win_width}x{self.win_height}")
        self.root.title("Employee management system")
        self.root.configure(bg="white")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=70)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.option_add("*Font", "Helvetica 12 bold")
        self.create_gui()

    # Create GUI
    def create_gui(self):
        self.em_in_frm = Frame(self.root, bg="white")
        self.em_in_frm.grid(row=0, column=0, sticky="nsew", padx=20)
        self.entries = []
        self.fields = [
            "first name",
            "last name",
            "job title",
            "salary",
            "email",
            "phone number",
        ]

        self.title1 = Label(
            self.em_in_frm,
            text="Add employee :",
            font=("Helvetica", 15, "bold"),
            bg="white",
        )
        self.title1.grid(row=0, column=0)

        # info entries
        for idx, field in enumerate(self.fields):
            lb_field = Label(self.em_in_frm, text=field, bg="white")
            lb_field.grid(row=idx + 1, column=0, sticky="nsw")
            lb_space = Label(self.em_in_frm, text=":", bg="white")
            lb_space.grid(row=idx + 1, column=1, sticky="nsw", padx=10)
            ent_field = Entry(self.em_in_frm, relief=GROOVE, borderwidth=2, bg="white")
            ent_field.grid(row=idx + 1, column=2, sticky="nsw", pady=10, ipady=2)
            self.entries.append(ent_field)
            ent_field.bind(
                "<Button-1>", lambda event, entry=ent_field: self.handle_error(entry)
            )

        # submit and cancel
        submit_btn = Button(
            self.em_in_frm,
            text="Submit",
            width=10,
            borderwidth=2,
            relief=GROOVE,
            command=lambda: add_em(self.table, self.entries),
        )
        submit_btn.grid(
            row=len(self.fields) + 1,
            column=0,
            pady=15,
            sticky="nsew",
        )
        cancel_btn = Button(
            self.em_in_frm,
            text="Cancel",
            relief=GROOVE,
            command=lambda: cancel(self.entries),
        )
        cancel_btn.grid(row=len(self.fields) + 1, column=2, pady=15, sticky="nsew")

        self.title2 = Label(
            self.em_in_frm,
            text="Delete employee :",
            font=("Helvetica", 15, "bold"),
            bg="white",
        )
        self.title2.grid(row=len(self.fields) + 2, column=0, pady=5)

        # delete and cancel
        opts = [
            "id",
            "first name",
            "last name",
            "email",
            "phone number",
        ]
        selected_opt = StringVar()
        selected_opt.set(opts[0])
        opt_menu = OptionMenu(self.em_in_frm, selected_opt, *opts)
        opt_menu.configure(relief=GROOVE, borderwidth=2)
        opt_menu.grid(row=len(self.fields) + 3, column=0, sticky="nsw", pady=10)

        del_space = Label(self.em_in_frm, text=":", bg="white")
        del_space.grid(row=len(self.fields) + 3, column=1, sticky="nsw", padx=10)

        del_field = Entry(self.em_in_frm, relief=GROOVE, borderwidth=2, bg="white")
        del_field.grid(
            row=len(self.fields) + 3, column=2, sticky="nsw", pady=10, ipady=2
        )
        del_field.bind(
            "<Button-1>", lambda event, entry=del_field: self.handle_error(entry)
        )

        del_btn = Button(
            self.em_in_frm,
            text="Delete",
            width=10,
            borderwidth=2,
            relief=GROOVE,
            command=lambda: del_em(self.table, del_field, selected_opt),
        )
        del_btn.grid(
            row=len(self.fields) + 4,
            column=0,
            pady=15,
            sticky="nsew",
        )
        cancel_del_btn = Button(
            self.em_in_frm,
            text="Cancel",
            relief=GROOVE,
            command=lambda: cancel(del_field),
        )
        cancel_del_btn.grid(row=len(self.fields) + 4, column=2, pady=15, sticky="nsew")

        # update employee
        up_opts = [
            "first name",
            "last name",
            "job title",
            "salary",
            "email",
            "phone number",
        ]
        self.title3 = Label(
            self.em_in_frm,
            text="Update employee :",
            font=("Helvetica", 15, "bold"),
            bg="white",
        )
        self.title3.grid(row=len(self.fields) + 5, column=0, pady=5)

        up_row = Label(self.em_in_frm, text="Row id", bg="white")
        up_row.grid(row=len(self.fields) + 6, column=0, sticky="nsw")
        up_lb_space = Label(self.em_in_frm, text=":", bg="white")
        up_lb_space.grid(row=len(self.fields) + 6, column=1, sticky="nsw", padx=10)
        up_spinbox = Spinbox(
            self.em_in_frm,
            width=18,
            from_=0,
            to=10**9,
            relief=GROOVE,
            borderwidth=2,
        )
        up_spinbox.grid(
            row=len(self.fields) + 6, column=2, sticky="nsw", pady=10, ipady=2
        )
        up_spinbox.bind(
            "<Button-1>", lambda event, entry=up_spinbox: self.handle_error(entry)
        )
        selected_up_opt = StringVar()
        selected_up_opt.set(up_opts[0])
        opt_up_menu = OptionMenu(self.em_in_frm, selected_up_opt, *up_opts)
        opt_up_menu.configure(relief=GROOVE, borderwidth=2)
        opt_up_menu.grid(row=len(self.fields) + 7, column=0, sticky="nsw", pady=10)

        up_space = Label(self.em_in_frm, text=":", bg="white")
        up_space.grid(row=len(self.fields) + 7, column=1, sticky="nsw", padx=10)

        up_field = Entry(self.em_in_frm, relief=GROOVE, borderwidth=2, bg="white")
        up_field.grid(
            row=len(self.fields) + 7, column=2, sticky="nsw", pady=10, ipady=2
        )
        up_field.bind(
            "<Button-1>", lambda event, entry=up_field: self.handle_error(entry)
        )

        up_btn = Button(
            self.em_in_frm,
            text="Update",
            width=10,
            borderwidth=2,
            relief=GROOVE,
            command=lambda: up_em(
                self.table, up_field, up_spinbox, selected_up_opt.get()
            ),
        )
        up_btn.grid(
            row=len(self.fields) + 8,
            column=0,
            pady=15,
            sticky="nsew",
        )
        cancel_up_btn = Button(
            self.em_in_frm,
            text="Cancel",
            relief=GROOVE,
            command=lambda: cancel(up_field),
        )
        cancel_up_btn.grid(row=len(self.fields) + 8, column=2, pady=15, sticky="nsew")

        quit_app = Button(
            self.em_in_frm,
            text="Quit app",
            relief=GROOVE,
            borderwidth=2,
            command=self.quit_app,
        )
        quit_app.grid(row=len(self.fields) + 9, column=0, pady=10, sticky="nsew")

        print_ems = Button(
            self.em_in_frm,
            text="Print employees",
            relief=GROOVE,
            borderwidth=2,
            command=lambda: print_employees(self.table),
        )
        print_ems.grid(row=len(self.fields) + 9, column=2, sticky="nsew", pady=10)

        # second Frame
        self.em_tb_frm = Frame(self.root, bg="white")
        self.em_tb_frm.grid(row=0, column=1, sticky="nsew")

        # second frame content
        tb_title = Label(
            self.em_tb_frm,
            text="Employees Table :",
            font=("Helvetica", 15, "bold"),
            bg="white",
        )
        tb_title.grid(row=0, column=0, sticky="w", pady=5)

        search_lb = Label(self.em_tb_frm, text="search by :", bg="white")
        search_lb.grid(row=1, column=0, sticky="nsew")

        srch_opts = [
            "id",
            "first name",
            "last name",
            "job title",
            "salary",
            "email",
            "phone number",
        ]
        search_opts_var = StringVar()
        search_opts_var.set(srch_opts[0])
        search_opts = OptionMenu(self.em_tb_frm, search_opts_var, *srch_opts)
        search_opts.configure(relief=GROOVE, borderwidth=2)
        search_opts.grid(row=1, column=1, sticky="w")

        search_ent = Entry(self.em_tb_frm, relief=GROOVE, borderwidth=2, bg="white")
        search_ent.bind(
            "<Key>",
            lambda event: key_pressed(search_ent, search_opts_var.get(), self.table),
        )
        search_ent.grid(row=1, column=2, sticky="nsew")

        order_by = Label(self.em_tb_frm, text="order by :", bg="white")
        order_by.grid(row=1, column=3, sticky="nsew")

        order_opts_var = StringVar()
        order_opts_var.set(srch_opts[0])
        order_opts_var.trace(
            "w", lambda *args: order_em(order_opts_var.get(), self.table)
        )
        order_opts = OptionMenu(self.em_tb_frm, order_opts_var, *srch_opts)
        order_opts.configure(relief=GROOVE, borderwidth=2)
        order_opts.grid(row=1, column=4, sticky="nsw")

        clear_em = Button(
            self.em_tb_frm,
            text="Clear",
            relief=GROOVE,
            borderwidth=2,
            command=lambda: clear(self.table),
        )
        clear_em.grid(row=1, column=5, sticky="nsew")

        # create table
        self.table_frm = Frame(self.em_tb_frm)
        self.table_frm.grid(row=2, column=0, columnspan=6, sticky="nsew", pady=5)

        scrollBar = ttk.Scrollbar(self.table_frm)
        scrollBar.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(
            self.table_frm,
            columns=tuple(srch_opts),
            yscrollcommand=scrollBar.set,
            show="headings",
        )

        self.table.column("#0", width=0, stretch=NO)
        self.table.column("id", width=40, anchor=CENTER)
        self.table.column("first name", width=150)
        self.table.column("last name", width=150)
        self.table.column("job title", width=150)
        self.table.column("salary", width=150)
        self.table.column("email", width=180)
        self.table.column("phone number", width=150)

        self.table.heading("id", text="id")
        self.table.heading("first name", text="first name", anchor=W)
        self.table.heading("last name", text="last name", anchor=W)
        self.table.heading("job title", text="job title", anchor=W)
        self.table.heading("salary", text="salary", anchor=W)
        self.table.heading("email", text="email", anchor=W)
        self.table.heading("phone number", text="phone number", anchor=W)

        load_data(self.table)

        self.table.pack(side=TOP, fill=BOTH, expand=True)
        scrollBar.config(command=self.table.yview)

        self.em_tb_frm.grid_columnconfigure(0, weight=1)
        self.em_tb_frm.grid_columnconfigure(1, weight=1)
        self.em_tb_frm.grid_columnconfigure(2, weight=1)
        self.em_tb_frm.grid_columnconfigure(3, weight=1)
        self.em_tb_frm.grid_columnconfigure(4, weight=1)
        self.em_tb_frm.grid_columnconfigure(5, weight=1)
        self.em_tb_frm.grid_rowconfigure(0, weight=0)
        self.em_tb_frm.grid_rowconfigure(1, weight=0)
        self.em_tb_frm.grid_rowconfigure(2, weight=1)

    # error handling
    def handle_error(self, entry):
        if (
            not entry.get()
            or entry.get().startswith("please")
            or entry.get().startswith("sorry")
        ):
            entry.configure(bg="white")
            entry.delete(0, END)

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    # Run program
    def start(self):
        self.root.mainloop()


app = Main()

app.start()
