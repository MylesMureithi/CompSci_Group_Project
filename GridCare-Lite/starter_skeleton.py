import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

utilities = pd.read_csv('National Electricity Grid Network Analysis/data_files/utilities.csv')  # utilities.csv
substations = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv')  # substations.csv
lines = pd.read_csv('National Electricity Grid Network Analysis/data_files/lines.csv')  # lines.csv

print("UTILITIES columns:", list(utilities.columns))
print("SUBSTATIONS columns:", list(substations.columns))
print("LINES columns:", list(lines.columns))


def init_db(db_path='gridcare.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'engineer', 'technician', 'customer_service'))
        )
        '''
    )

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS substations (
            substation_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            region TEXT NOT NULL
        )
        '''
    )

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS outages (
            outage_id INTEGER PRIMARY KEY AUTOINCREMENT,
            substation_id INTEGER NOT NULL,
            reported_by INTEGER NOT NULL,
            description TEXT,
            severity TEXT DEFAULT 'Medium' CHECK (severity IN ('Low', 'Medium', 'High')),
            status TEXT DEFAULT 'Open' CHECK (status IN ('Open', 'In Progress', 'Resolved')),
            reported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            resolved_at TEXT,
            FOREIGN KEY (substation_id) REFERENCES substations(substation_id),
            FOREIGN KEY (reported_by) REFERENCES users(user_id)
        )
        '''
    )

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS work_orders (
            work_order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            outage_id INTEGER NOT NULL,
            assigned_technician INTEGER,
            scheduled_date TEXT,
            status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'Scheduled', 'Completed')),
            FOREIGN KEY (outage_id) REFERENCES outages(outage_id),
            FOREIGN KEY (assigned_technician) REFERENCES users(user_id)
        )
        '''
    )


    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            description TEXT NOT NULL,
            outage_id INTEGER,
            submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (outage_id) REFERENCES outages(outage_id)
        )
        '''
    )

    # --- Load substations from CSV, WITHOUT destroying the table schema above ---
    # NOTE: to_sql(..., if_exists='replace') was dropping and rebuilding this table
    # using whatever columns happen to be in the CSV, which wipes out the
    # PRIMARY KEY and can break the outages.substation_id foreign key.
    # This version only inserts rows if the CSV actually has the columns
    # this table expects (substation_id, name, region). If it doesn't,
    # it tells you instead of silently corrupting the table.
    try:
        substations_df = pd.read_csv('National Electricity Grid Network Analysis/data_files/substations.csv')
        expected_cols = {'substation_id', 'name', 'region'}
        csv_cols = set(substations_df.columns.str.lower().str.replace(' ', '_'))

        if expected_cols.issubset(csv_cols):
            substations_df.columns = substations_df.columns.str.lower().str.replace(' ', '_')
            rows = substations_df[['substation_id', 'name', 'region']].values.tolist()
            cur.executemany(
                'INSERT OR IGNORE INTO substations (substation_id, name, region) VALUES (?, ?, ?)',
                rows
            )
        else:
            print(
                "Skipped loading substations.csv: its columns "
                f"({list(substations_df.columns)}) don't match what the "
                "substations table expects (substation_id, name, region). "
                "Check with your team on the real column mapping before loading this."
            )
    except Exception as e:
        print(f"Could not load substations CSV: {e}")

    # Seed a test admin user so login works
    cur.execute(
        '''
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        ''',
        ('admin', 'password123', 'admin')
    )

        # Seed additional technician users for demo purposes
    cur.execute(
        '''
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        ''',
        ('tech1', 'password123', 'technician')
    )
    conn.commit()
    return conn


class LoginWindow(tk.Frame):
    def __init__(self, master, conn, on_success):
        super().__init__(master)
        self.conn = conn
        self.on_success = on_success
        self.master = master
        master.title('GridCare-Lite — Login')

        ttk.Label(self, text='Username:').grid(row=0, column=0, padx=8, pady=8, sticky='e')
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(self, text='Password:').grid(row=1, column=0, padx=8, pady=8, sticky='e')
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.grid(row=1, column=1, padx=8, pady=8)

        ttk.Button(self, text='Log In', command=self.attempt_login).grid(row=2, column=0, columnspan=2, pady=10)
        self.pack(padx=20, pady=20)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror('Login Failed', 'Please enter both a username and password.')
            return

        cur = self.conn.cursor()
        cur.execute('SELECT user_id, password_hash, role FROM users WHERE username = ?', (username,))
        row = cur.fetchone()

        if row and row[1] == password:
            user_id, _, role = row
            self.on_success(user_id, username, role)
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password.')


class OutageDashboard(tk.Frame):
    def __init__(self, master, conn, user_id, username, role):
        super().__init__(master)
        self.conn = conn
        self.user_id = user_id
        self.role = role
        master.title(f'GridCare-Lite — Outage Dashboard ({username})')

        columns = ('outage_id', 'substation_id', 'description', 'status', 'reported_at')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Button(self, text='Refresh', command=self.load_outages).pack(pady=5)
        ttk.Button(self, text='Add Outage', command=self.open_new_outage_form).pack(pady=5)
        ttk.Button(self, text='Log Complaint', command=self.open_complaint_form).pack(pady=5)
        ttk.Button(self, text='Reports', command=self.open_reports).pack(pady=5)


        if self.role == 'admin':
            ttk.Button(self, text='Assign Work Order', command=self.open_assign_form).pack(pady=5) 

        self.pack(fill='both', expand=True)
        self.load_outages()

    def load_outages(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cur = self.conn.cursor()
        cur.execute('SELECT outage_id, substation_id, description, status, reported_at FROM outages')
        for row in cur.fetchall():
            self.tree.insert('', 'end', values=row)

    def open_new_outage_form(self):
        NewOutageForm(self.master, self.conn, self.user_id, on_submit=self.load_outages)

        
    def open_assign_form(self):
        AssignWorkOrderForm(self.master, self.conn, on_submit=self.load_outages)   

    def open_complaint_form(self):
        ComplaintForm(self.master, self.conn, on_submit=self.load_outages)  


    def open_reports(self):
        ReportsView(self.master, self.conn)      


# Part 3: Creating the New Outage Dashboard from the question

class NewOutageForm(tk.Toplevel):
    def __init__(self, master, conn, user_id, on_submit):
        super().__init__(master)
        self.conn = conn
        self.user_id = user_id
        self.on_submit = on_submit
        self.title('Report New Outage')

        cur = self.conn.cursor()
        cur.execute('SELECT substation_id, name FROM substations')
        self.substations = cur.fetchall()

        # Adding the new titles for the new form outage class

        ttk.Label(self, text='Substation:').grid(row=0, column=0, padx=8, pady=8, sticky='e')
        substation_names = [f"{sid} — {name}" for sid, name in self.substations]
        self.substation_combo = ttk.Combobox(self, values=substation_names, state='readonly')
        self.substation_combo.grid(row=0, column=1, padx=8, pady=8)

        # Adding the description tab that is required

        ttk.Label(self, text='Description:').grid(row=1, column=0, padx=8, pady=8, sticky='e')
        self.description_entry = ttk.Entry(self, width=40)
        self.description_entry.grid(row=1, column=1, padx=8, pady=8)

        # Adding the severity tab required

        ttk.Label(self, text='Severity:').grid(row=2, column=0, padx=8, pady=8, sticky='e')
        self.severity_combo = ttk.Combobox(self, values=['Low', 'Medium', 'High'], state='readonly')
        self.severity_combo.grid(row=2, column=1, padx=8, pady=8)
        self.severity_combo.set('Medium')

        # Adding the submit button for submitting the form

        ttk.Button(self, text='Submit Form', command=self.submit_outage).grid(row=3, column=0, columnspan=2, pady=10)

    # Initialising the getters

    def submit_outage(self):
        selected = self.substation_combo.get()
        description = self.description_entry.get()
        severity = self.severity_combo.get()

        # Logic to handle the wrong input of data or information into the form

        if not selected or not description:
            messagebox.showerror('Missing Info', 'Please select a substation and enter a description.')
            return

        substation_id = int(selected.split(' — ')[0])

        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO outages (substation_id, reported_by, description, severity) VALUES (?, ?, ?, ?)',
            (substation_id, self.user_id, description, severity)
        )
        self.conn.commit()

        self.on_submit()
        self.destroy()

# Part 4: Work order assignment screen (admin only)

class AssignWorkOrderForm(tk.Toplevel):
    def __init__(self, master, conn, on_submit):
        super().__init__(master)
        self.conn = conn
        self.on_submit = on_submit
        self.title('Assign Work Order')

        cur = self.conn.cursor()
        cur.execute("SELECT outage_id, description FROM outages WHERE status != 'Resolved'")
        self.outages = cur.fetchall()
        cur.execute("SELECT user_id, username FROM users WHERE role = 'technician'")
        self.technicians = cur.fetchall()

# Adding the Outage tab

        ttk.Label(self, text='Outage:').grid(row=0, column=0, padx=8, pady=8, sticky='e')
        outage_labels = [f"{oid} — {desc}" for oid, desc in self.outages]
        self.outage_combo = ttk.Combobox(self, values=outage_labels, state='readonly', width=40)
        self.outage_combo.grid(row=0, column=1, padx=8, pady=8)

# Adding the technician tab

        ttk.Label(self, text='Technician:').grid(row=1, column=0, padx=8, pady=8, sticky='e')
        tech_labels = [f"{tid} — {name}" for tid, name in self.technicians]
        self.tech_combo = ttk.Combobox(self, values=tech_labels, state='readonly')
        self.tech_combo.grid(row=1, column=1, padx=8, pady=8)

# Adding the scheduled day by the admin

        ttk.Label(self, text='Scheduled Date (YYYY-MM-DD):').grid(row=2, column=0, padx=8, pady=8, sticky='e')
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=2, column=1, padx=8, pady=8)

# Adding the assign button

        ttk.Button(self, text='Assign', command=self.submit_assignment).grid(row=3, column=0, columnspan=2, pady=10)

# Initialising the getters for the parameters

    def submit_assignment(self):
        outage_sel = self.outage_combo.get()
        tech_sel = self.tech_combo.get()
        date = self.date_entry.get()

# Logic to handle errors with missing information

        if not outage_sel or not tech_sel or not date:
            messagebox.showerror('Missing Info', 'Please fill in all fields.')
            return

        outage_id = int(outage_sel.split(' — ')[0])
        tech_id = int(tech_sel.split(' — ')[0])

        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO work_orders (outage_id, assigned_technician, scheduled_date) VALUES (?, ?, ?)',
            (outage_id, tech_id, date)
        )
        self.conn.commit()

        self.on_submit()
        self.destroy()

# Part5: Creating the technicians view to see assigned jobs

class TechnicianView(tk.Frame):
    def __init__(self, master, conn, user_id, username):
        super().__init__(master)
        self.conn = conn
        self.user_id = user_id
        master.title(f'GridCare-Lite — My Work Orders ({username})')

        columns = ('work_order_id', 'outage_id', 'description', 'scheduled_date', 'status')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Button(self, text='Refresh', command=self.load_work_orders).pack(pady=5)
        ttk.Button(self, text='Mark Complete', command=self.mark_complete).pack(pady=5)
        self.pack(fill='both', expand=True)
        self.load_work_orders()

    def load_work_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT work_orders.work_order_id, outages.outage_id, outages.description,
                   work_orders.scheduled_date, work_orders.status
            FROM work_orders
            JOIN outages ON work_orders.outage_id = outages.outage_id
            WHERE work_orders.assigned_technician = ?
            ''',
            (self.user_id,)
        )
        for row in cur.fetchall():
            self.tree.insert('', 'end', values=row)

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror('No Selection', 'Please select a work order first.')
            return
        values = self.tree.item(selected[0])['values']
        work_order_id, outage_id = values[0], values[1]

        cur = self.conn.cursor()
        cur.execute(
            "UPDATE work_orders SET status = 'Completed' WHERE work_order_id = ?",
            (work_order_id,)
        )
        cur.execute(
            "UPDATE outages SET status = 'Resolved', resolved_at = CURRENT_TIMESTAMP WHERE outage_id = ?",
            (outage_id,)
        )
        self.conn.commit()
        self.load_work_orders()

# Part 6: Creating a new class for the customer complaint log

class ComplaintForm(tk.Toplevel):
    def __init__(self, master, conn, on_submit):
        super().__init__(master)
        self.conn = conn
        self.on_submit = on_submit
        self.title('Customer Complaint')

        cur = self.conn.cursor()
        cur.execute("SELECT outage_id, description FROM outages")
        self.outages = cur.fetchall()

        ttk.Label(self, text='Customer Name:').grid(row=0, column=0, padx=8, pady=8, sticky='e')
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(self, text='Description:').grid(row=1, column=0, padx=8, pady=8, sticky='e')
        self.description_entry = ttk.Entry(self, width=40)
        self.description_entry.grid(row=1, column=1, padx=8, pady=8)

        ttk.Label(self, text='Related Outage (optional):').grid(row=2, column=0, padx=8, pady=8, sticky='e')
        outage_labels = ['None'] + [f"{oid} — {desc}" for oid, desc in self.outages]
        self.outage_combo = ttk.Combobox(self, values=outage_labels, state='readonly', width=40)
        self.outage_combo.set('None')
        self.outage_combo.grid(row=2, column=1, padx=8, pady=8)

        ttk.Button(self, text='Submit Complaint', command=self.submit_complaint).grid(row=3, column=0, columnspan=2, pady=10)

    def submit_complaint(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        outage_sel = self.outage_combo.get()

        if not name or not description:
            messagebox.showerror('Missing Info', 'Please enter a name and description.')
            return

        outage_id = None
        if outage_sel != 'None':
            outage_id = int(outage_sel.split(' — ')[0])

        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO complaints (customer_name, description, outage_id) VALUES (?, ?, ?)',
            (name, description, outage_id)
        )
        self.conn.commit()

        self.on_submit()
        self.destroy()


class ReportsView(tk.Toplevel):
    def __init__(self, master, conn):
        super().__init__(master)
        self.conn = conn
        self.title('Reports')

        cur = self.conn.cursor()

        cur.execute("SELECT status, COUNT(*) FROM outages GROUP BY status")
        outage_counts = dict(cur.fetchall())

        cur.execute("SELECT COUNT(*) FROM complaints")
        complaint_count = cur.fetchone()[0]

        cur.execute("SELECT status, COUNT(*) FROM work_orders GROUP BY status")
        work_order_counts = dict(cur.fetchall())

        row = 0
        ttk.Label(self, text='Outage Summary', font=('', 11, 'bold')).grid(row=row, column=0, columnspan=2, padx=10, pady=(10, 4), sticky='w')
        row += 1
        for status in ('Open', 'In Progress', 'Resolved'):
            ttk.Label(self, text=f'{status}:').grid(row=row, column=0, padx=10, sticky='e')
            ttk.Label(self, text=str(outage_counts.get(status, 0))).grid(row=row, column=1, padx=10, sticky='w')
            row += 1

        ttk.Label(self, text='Work Order Summary', font=('', 11, 'bold')).grid(row=row, column=0, columnspan=2, padx=10, pady=(10, 4), sticky='w')
        row += 1
        for status in ('Pending', 'Scheduled', 'Completed'):
            ttk.Label(self, text=f'{status}:').grid(row=row, column=0, padx=10, sticky='e')
            ttk.Label(self, text=str(work_order_counts.get(status, 0))).grid(row=row, column=1, padx=10, sticky='w')
            row += 1

        ttk.Label(self, text='Complaints Logged:').grid(row=row, column=0, padx=10, pady=(10, 10), sticky='e')
        ttk.Label(self, text=str(complaint_count)).grid(row=row, column=1, padx=10, pady=(10, 10), sticky='w')

def main():
    conn = init_db()
    root = tk.Tk()

    def show_dashboard(user_id, username, role):
        for widget in root.winfo_children():
            widget.destroy()
        if role == 'technician':
            TechnicianView(root, conn, user_id, username)
        else:
            OutageDashboard(root, conn, user_id, username, role)

    LoginWindow(root, conn, on_success=show_dashboard)
    root.mainloop()

def inspect_database(conn):
    cur = conn.cursor()
    print("--- USERS TABLE ---")
    cur.execute("SELECT user_id, username, role FROM users")
    for row in cur.fetchall():
        print(row)


if __name__ == '__main__':
    database_conn = init_db()
    inspect_database(database_conn)
    database_conn.close()

    main()
