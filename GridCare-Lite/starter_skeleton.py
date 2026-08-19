import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


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

#--- Adding a Test user seed to see if system woorks
    cur.execute(
        '''
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)            
        ''',
        ('admin','password123','admin')
    )
    conn.commit()
    return conn

"""if __name__ == "__main__":
    conn = init_db()
    conn.close()
    print("Database initialized successfully!")"""


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
        
        # Real database check against the users table
        cur = self.conn.cursor()
        cur.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        row = cur.fetchone()

        if row and row[0] == password:
            self.on_success(username)
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password.')
        self.on_success(username)


class OutageDashboard(tk.Frame):
    def __init__(self, master, conn, username):
        super().__init__(master)
        self.conn = conn
        master.title(f'GridCare-Lite — Outage Dashboard ({username})')

        columns = ('outage_id', 'substation_id', 'description', 'status', 'reported_at')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)


        ttk.Button(self, text='Refresh', command=self.load_outages).pack(pady=5)
        self.pack(fill='both', expand=True)
        self.load_outages()


def load_outages(self):
    for row in self.tree.get_children():
        self.tree.delete(row)
    cur = self.conn.cursor()
    cur.execute('SELECT outage_id, substation_id, description, status, reported_at FROM outages')
    for row in cur.fetchall():
        self.tree.insert('', 'end', values=row)


def main():
    conn = init_db() # Check line 6
    root = tk.Tk()

    def show_dashboard(username):
        for widget in root.winfo_children():
            widget.destroy()
        OutageDashboard(root, conn, username)

    LoginWindow(root, conn, on_success=show_dashboard)
    root.mainloop()


if __name__ == '__main__':
    main()