import sqlite3
from tkinter import *
from tkinter import messagebox
#from adminWindow import view_assignment_details, view_assignments_window

#user can view assignment + update status

def get_db_connection():
    return sqlite3.connect('assignments.db')

def assigned_interface():
    assigned_frame = Frame(root)
    Label(assigned_frame, text="User Dashboard", font=("Georgia", 16)).grid(row=0, column=0, columnspan=2, pady=10)
    Button(assigned_frame, text="View All Assignments", width=25, font=("Georgia", 12), command=lambda: view_assignments_window(root,"assigned")).grid(row=1, column=0, padx=5, pady=5)
    assigned_frame.pack(pady=20)

def view_assignments_window(role):
    win = Toplevel(root)
    win.geometry("300x200")
    win.title("All Assignments")
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM assignments")
    assignments = c.fetchall()
    conn.close()
    
    if assignments:
        for assignment in assignments:
            assignment_str = assignment[1]
            # Use a lambda with default argument to capture the current assignment id
            Button(win, text=assignment_str, command=lambda a_id=assignment[0]: view_assignment_details(a_id, role)).pack(padx=10, pady=5)
    else:
        Label(win, text="No assignments found.", font=("Helvetica", 12)).pack(padx=10, pady=10)

def view_assignment_details(assignment_id, role):
    win = Toplevel(root)
    win.title("Assignment Details")
    win.geometry("300x200")
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM assignments WHERE id=?", (assignment_id,))
    assignment = c.fetchone()
    conn.close()
    
    if not assignment:
        messagebox.showerror("Error", "Assignment not found.")
        win.destroy()
        return

    # assignment: (id, name, due_date, description, status, people_involved)
    Label(win, text=f"Name: {assignment[1]}", font=("Helvetica", 12)).grid(row=0, column=0, sticky=W, padx=10, pady=5)
    Label(win, text=f"Due Date: {assignment[2]}", font=("Helvetica", 12)).grid(row=1, column=0, sticky=W, padx=10, pady=5)
    Label(win, text=f"Description: {assignment[3]}", font=("Helvetica", 12)).grid(row=2, column=0, sticky=W, padx=10, pady=5)
    Label(win, text=f"Status: {assignment[4]}", font=("Helvetica", 12)).grid(row=3, column=0, sticky=W, padx=10, pady=5)
    Label(win, text=f"People Involved: {assignment[5]}", font=("Helvetica", 12)).grid(row=4, column=0, sticky=W, padx=10, pady=5)
    
    if role == "admin":
        Button(win, text="Edit Assignment", font=("Helvetica", 12), command=lambda: edit_assignment_window(assignment)).grid(row=5, column=0, pady=10)
    elif role == "assigned":
        # Assigned users can update the status of the assignment
        Label(win, text="Update Status:", font=("Helvetica", 12)).grid(row=5, column=0, sticky=W, padx=10, pady=5)
        status_var = StringVar(win)
        status_var.set(assignment[4])
        OptionMenu(win, status_var, "completed", "not completed" ).grid(row=5, column=1, padx=10, pady=5)
        
        def update_status():
            new_status = status_var.get()
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("UPDATE assignments SET status=? WHERE id=?", (new_status, assignment_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Status updated!")
            win.destroy()
        Button(win, text="Update Status", font=("Helvetica", 12), command=update_status).grid(row=6, column=0, columnspan=2, pady=10)


#TESTINGG:
if __name__ == "__main__":
    from tkinter import Tk

    root = Tk()
    root.withdraw()  # hide the root window if you only want the view window

    # Call the function with test values
    view_assignments_window( role="assigned")

    root.mainloop()
