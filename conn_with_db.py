import sqlite3
from tkinter import *  # type:ignore
from tabulate import tabulate
from fpdf import FPDF


# cancel adding or deleting or updating
def cancel(data):
    if type(data) == list:
        for entry in data:
            entry.delete(0, END)
    else:
        data.delete(0, END)


# raise error
def raise_error(obj, error):
    obj.delete(0, "end")
    obj.config(bg="#d84f4f")
    obj.insert(0, error)
    raise ValueError()


# load employees
def load_data(tb):
    conn = sqlite3.connect("employees7.db")
    cr = conn.cursor()

    cr.execute("SELECT * FROM EMPLOYEES")
    data = cr.fetchall()

    try:
        tb.delete(*tb.get_children())
        for employee in data:
            tb.insert("", END, text=employee[0], values=employee)
    finally:
        conn.commit()
        conn.close()


# clear employees
def clear(tb):
    conn = sqlite3.connect("employees7.db")
    cr = conn.cursor()
    cr.execute("DELETE FROM EMPLOYEES")
    conn.commit()
    conn.close()
    load_data(tb)


# print employees
def print_employees(tb):
    conn = sqlite3.connect("employees7.db")
    cr = conn.cursor()
    # Execute a SELECT query
    cr.execute("SELECT * FROM EMPLOYEES")
    rows = cr.fetchall()

    # Get the table column names
    column_names = [description[0] for description in cr.description]

    # Close the database connection
    conn.close()

    # Convert rows and column names to a table string using tabulate
    table_str = tabulate(rows, headers=column_names, tablefmt="grid")

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, table_str)
    pdf.output("table_report.pdf")


# order employees
def order_em(val, tb):
    conn = sqlite3.connect("employees7.db")
    cr = conn.cursor()
    cr.execute(
        f"""SELECT * FROM EMPLOYEES ORDER BY {"ID" if val == "id" else "FIRST_NAME" if val == "first name" else "LAST_NAME" if val =="last name" else "JOB_TITLE" if val == "job title" else "SALARY" if val == "salary" else "EMAIL" if val == "email" else "PHONE_NUMBER"} """
    )
    data = cr.fetchall()

    try:
        tb.delete(*tb.get_children())
        for employee in data:
            tb.insert("", END, text=employee[0], values=employee)
    finally:
        conn.commit()
        conn.close()


def key_pressed(search_ent, search_opts_var, tb):
    search_ent.after(10, lambda: search_em(tb, search_ent.get(), search_opts_var))


# search employee
def search_em(tb, input, val):
    conn = sqlite3.connect("employees7.db")
    cr = conn.cursor()

    cr.execute(
        f"""SELECT * FROM EMPLOYEES WHERE {"ID" if val == "id" else "FIRST_NAME" if val == "first name" else "LAST_NAME" if val =="last name" else "JOB_TITLE" if val == "job title" else "SALARY" if val == "salary" else "EMAIL" if val == "email" else "PHONE_NUMBER"} LIKE '%{input}%'"""
    )

    rows = cr.fetchall()
    try:
        tb.delete(*tb.get_children())
        for employee in rows:
            tb.insert("", END, text=employee[0], values=employee)
    finally:
        conn.commit()
        conn.close()

    # print("-" * 10)
    # for row in rows:
    #     print(row)
    # print("-" * 10)


# add employee
def add_em(tb, data):
    DATA = []
    conn = sqlite3.connect("employees7.db")
    cr = conn.cursor()

    cr.execute(
        "CREATE TABLE IF NOT EXISTS EMPLOYEES(ID INTEGER,FIRST_NAME TEXT,LAST_NAME TEXT,JOB_TITLE TEXT,SALARY INTEGER, EMAIL TEXT,PHONE_NUMBER INTEGER)"
    )
    cr.execute(f"SELECT rowid FROM EMPLOYEES")

    rowid = len(cr.fetchall()) + 1
    try:
        for em in data:
            if em.get():
                DATA.append(em.get())
                em.delete(0, END)
            else:
                raise_error(em, "please fill the field")
    except ValueError:
        DATA.clear()
    else:
        cr.execute(
            f"INSERT INTO EMPLOYEES(ID,FIRST_NAME,LAST_NAME,JOB_TITLE,SALARY, EMAIL,PHONE_NUMBER) VALUES({rowid},?,?,?,?,?,?)",
            DATA,  # type: ignore
        )

    conn.commit()
    conn.close()
    load_data(tb)


# delete employee
def del_em(tb, val, selected_op):
    conn = sqlite3.connect("employees7.db")
    cr = conn.cursor()
    value = ""
    result = tuple()
    try:
        if val.get():
            value = val.get()
            val.delete(0, END)
            cr.execute(
                f"""SELECT * FROM EMPLOYEES WHERE {"ID" if selected_op.get() == "id" else "FIRST_NAME" if selected_op.get() == "first name"
                            else "LAST_NAME" if selected_op.get() =="last name"
                            else "EMAIL" if selected_op.get() == 'email'
                            else "PHONE_NUMBER" } LIKE '%{value}%'"""
            )

            result = cr.fetchall()

            if len(result) > 1:
                raise_error(val, "please more specific")
            elif len(result) == 0:
                raise_error(val, "sorry, no such employee")

        else:
            raise_error(val, "please fill the field")
    except ValueError:
        pass
    else:
        cr.execute(
            f"""DELETE FROM EMPLOYEES WHERE {"ID" if selected_op.get() == "id" else "FIRST_NAME" if selected_op.get() == "first name"
                            else "LAST_NAME" if selected_op.get() =="last name"
                            else "EMAIL" if selected_op.get() == 'email'
                            else "PHONE_NUMBER"} LIKE '%{value}%'"""
        )
        cr.execute(f"""UPDATE EMPLOYEES SET ID = ID -1 WHERE ID > {result[0][0]}""")

    conn.commit()
    conn.close()
    load_data(tb)


# update employee
def up_em(tb, val, row_id, selected_val):
    conn = sqlite3.connect("employees7.db")
    cr = conn.cursor()
    cr.execute("SELECT * FROM EMPLOYEES")
    rows = cr.fetchall()

    try:
        if row_id.get() == "0":
            raise_error(row_id, "please enter row id")
        elif int(row_id.get()) > len(rows):
            raise_error(row_id, "please enter a valid row id")

        if not val.get():
            raise_error(val, f"please enter a valid {selected_val}")

    except ValueError:
        pass
    else:
        cr.execute(
            f"""UPDATE EMPLOYEES SET {"FIRST_NAME" if selected_val == 'first name'
            else "LAST_NAME" if selected_val=="last name"
            else "JOB_TITLE" if selected_val=="job title"
            else "SALARY" if selected_val=="salary"
            else "EMAIL" if selected_val=="email"
            else "PHONE_NUMBER"} = '{val.get()}' WHERE ID = {row_id.get()}"""
        )
        cancel(row_id)
        cancel(val)
        conn.commit()
        conn.close()
        load_data(tb)
