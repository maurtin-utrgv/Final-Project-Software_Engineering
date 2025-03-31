import sqlite3
from tkinter import *
from tkinter import messagebox

# ------------------------------------------
# Database Setup
# ------------------------------------------
def init_db():
    conn = sqlite3.connect('assignments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    due_date TEXT,
                    description TEXT,
                    status TEXT,
                    people_involved TEXT
                )''')
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('assignments.db')

init_db()

# ------------------------------------------
# Main Application Setup
# ------------------------------------------
root = Tk()
root.title("To‑Do List Application")
root.geometry("500x400")

# Global variable to store the user role
user_role = StringVar()

# ------------------------------------------
# Login / Role Selection Frame
# ------------------------------------------
login_frame = Frame(root)
Label(login_frame, text="Select User Type:", font=("Georgia", 14)).grid(row=0, column=0, columnspan=2, pady=10)
Radiobutton(login_frame, text="Admin (Assign Tasks)", variable=user_role, value="admin", font=("Georgia", 12)).grid(row=1, column=0, sticky=W, padx=10)
Radiobutton(login_frame, text="Assigned User", variable=user_role, value="assigned", font=("Georgia", 12)).grid(row=2, column=0, sticky=W, padx=10)
Button(login_frame, text="Continue", font=("Georgia", 12), command=lambda: login(user_role.get())).grid(row=3, column=0, columnspan=2, pady=20)
login_frame.pack(pady=30)

def login(role):
    if role not in ["admin", "assigned"]:
        messagebox.showerror("Error", "Please select a user type.")
        return
    login_frame.pack_forget()  # Hide the login frame
    if role == "admin":
        admin_interface()
    else:
        assigned_interface()

# ------------------------------------------
# Admin Interface (can create, edit, delete)
# ------------------------------------------
def admin_interface():
    admin_frame = Frame(root)
    Label(admin_frame, text="Admin Dashboard", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
    Button(admin_frame, text="Create New Assignment", width=25, font=("Helvetica", 12), command=create_assignment_window).grid(row=1, column=0, padx=5, pady=5)
    Button(admin_frame, text="View All Assignments", width=25, font=("Helvetica", 12), command=lambda: view_assignments_window("admin")).grid(row=1, column=1, padx=5, pady=5)
    admin_frame.pack(pady=20)

# ------------------------------------------
# Assigned User Interface (view & update status)
# ------------------------------------------
def assigned_interface():
    assigned_frame = Frame(root)
    Label(assigned_frame, text="User Dashboard", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
    Button(assigned_frame, text="View All Assignments", width=25, font=("Helvetica", 12), command=lambda: view_assignments_window("assigned")).grid(row=1, column=0, padx=5, pady=5)
    assigned_frame.pack(pady=20)



#Call the main loop for displaying the root window
root.mainloop()


