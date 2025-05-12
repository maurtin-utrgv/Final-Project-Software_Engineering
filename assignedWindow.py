import sqlite3
from tkinter import *
from tkinter import messagebox
from adminWindow import get_db_connection, view_assignment_details

# ------------------------------------------
# Assigned User Interface
# ------------------------------------------

def assigned_interface(root, current_user):
    """
    Display the assigned-user dashboard: lets a user view and update only their own assignments.

    Args:
        root (Tk): the main Tkinter root window
        current_user (str): username of the logged-in user
    """
    frame = Frame(root)

    def logout():
        from Login_page import login_gui
        """Close assigned-user dashboard and return to login."""
        root.destroy()
        login_gui()

    Label(frame, text=f"Welcome, {current_user}", font=("Helvetica", 16)).grid(row=0, column=0, pady=10)
    
    Button(
        frame,
        text="View My Assignments",
        width=25,
        font=("Helvetica", 12),
        command=lambda: view_assignments_window(root, "assigned", current_user)
    ).grid(row=1, column=0, pady=5)

    Button(frame, text="Logout", width=25, font=("Helvetica", 12), fg="red", command=logout) \
        .grid(row=2, column=0, pady=(10,0))

    frame.pack(pady=20)
# ------------------------------------------
# View Assignments (Assigned User)
# ------------------------------------------

def view_assignments_window(root, role, current_user=None):
    """
    Pop up a window listing the assignments for the current_user. Clicking one opens detail/update.

    Args:
        root (Tk): the main Tkinter root window
        role (str): should be "assigned" when used here
        current_user (str): username to filter assignments by
    """
    win = Toplevel(root)
    win.title("My Assignments")
    win.geometry("300x200")

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM assignments")
    assignments = c.fetchall()
    conn.close()

    if assignments:
        found = False
        for assignment in assignments:
            # assignment tuple: (id, name, due_date, desc, status, people_involved)
            people = [p.strip() for p in assignment[5].split(",")]
            if current_user not in people:
                continue
            found = True
            Button(
                win,
                text=assignment[1],  # show assignment name
                width=30,
                command=lambda a_id=assignment[0]: view_assignment_details(a_id, "assigned")
            ).pack(padx=10, pady=5)
        if not found:
            Label(win, text="No assignments assigned to you.", font=("Helvetica", 12)).pack(padx=10, pady=10)
    else:
        Label(win, text="No assignments found.", font=("Helvetica", 12)).pack(padx=10, pady=10)