import sqlite3
from tkinter import *
from tkinter import messagebox


# -------------------------------
# Database Functions
# -------------------------------
def get_db_connection():
    # Connect to the SQLite database (or create it if it doesn't exist)
    #conn = sqlite3.connect('toDoListAssignments.db')
    conn = sqlite3.connect('assignments.db')
    return conn

def initialize_db():
    # Create the assignments table if it doesn't exist
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT,
            description TEXT,
            status TEXT,
            people_involved TEXT
        )
    ''')
    conn.commit()
    conn.close()



# ------------------------------------------
# Admin Interface (can create, edit, delete)
# ------------------------------------------
def admin_interface():
    admin_frame = Frame(root)
    Label(admin_frame, text="Admin Dashboard", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
    Button(admin_frame, text="Create New Assignment", width=25, font=("Helvetica", 12), command=create_assignment_window).grid(row=1, column=0, padx=5, pady=5)
    Button(admin_frame, text="View/Edit All Assignments", width=25, font=("Helvetica", 12), command=lambda: view_assignments_window("admin")).grid(row=1, column=1, padx=5, pady=5)
    admin_frame.pack(pady=20)



# ------------------------------------------
# Create New Assignment Window (Admin Only)
# ------------------------------------------
def create_assignment_window():
    win = Toplevel(root)
    win.title("Create New Assignment")
    
    # Labels and entry fields
    Label(win, text="Name:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
    Label(win, text="Due Date:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
    Label(win, text="Description:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
    Label(win, text="Status:").grid(row=3, column=0, sticky=E, padx=5, pady=5)
    Label(win, text="People Involved:").grid(row=4, column=0, sticky=E, padx=5, pady=5)
    
    name_entry = Entry(win, width=30)
    due_date_entry = Entry(win, width=30)
    description_entry = Entry(win, width=30)
    status_var = StringVar(win)
    status_var.set("not completed") #default value
    people_entry = Entry(win, width=30)
    
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    due_date_entry.grid(row=1, column=1, padx=5, pady=5)
    description_entry.grid(row=2, column=1, padx=5, pady=5)
    OptionMenu(win, status_var, "completed", "not completed").grid(row=3, column=1, padx=5, pady=5)
    people_entry.grid(row=4, column=1, padx=5, pady=5)
    
    def submit_assignment():
        name = name_entry.get()
        due_date = due_date_entry.get()
        description = description_entry.get()
        status = status_var.get()
        people = people_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO assignments (name, due_date, description, status, people_involved) VALUES (?, ?, ?, ?, ?)",
                  (name, due_date, description, status, people))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Assignment created successfully!")
        win.destroy()
    
    Button(win, text="Submit", command=submit_assignment).grid(row=5, column=0, columnspan=2, pady=10)

# ------------------------------------------
# View/Edit Assignment Details Window
# ------------------------------------------
def view_assignment_details(assignment_id, role):
    win = Toplevel(root)
    win.title("Assignment Details")
    
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

# ------------------------------------------
# Edit Assignment Window (Admin Only)
# ------------------------------------------
def edit_assignment_window(assignment):
    win = Toplevel(root)
    win.title("Edit Assignment")
    
    Label(win, text="Name:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
    Label(win, text="Due Date:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
    Label(win, text="Description:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
    Label(win, text="Status:").grid(row=3, column=0, sticky=E, padx=5, pady=5)
    Label(win, text="People Involved:").grid(row=4, column=0, sticky=E, padx=5, pady=5)
    
    name_entry = Entry(win, width=30)
    due_date_entry = Entry(win, width=30)
    description_entry = Entry(win, width=30)
    status_var = StringVar(win)
    status_var.set(assignment[4])
    people_entry = Entry(win, width=30)
    
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    due_date_entry.grid(row=1, column=1, padx=5, pady=5)
    description_entry.grid(row=2, column=1, padx=5, pady=5)
    OptionMenu(win, status_var, "completed", "not completed").grid(row=3, column=1, padx=5, pady=5)
    people_entry.grid(row=4, column=1, padx=5, pady=5)
    
    # Pre-fill the fields with the current data
    name_entry.insert(0, assignment[1])
    due_date_entry.insert(0, assignment[2])
    description_entry.insert(0, assignment[3])
    people_entry.insert(0, assignment[5])
    
    def submit_edit():
        new_name = name_entry.get()
        new_due = due_date_entry.get()
        new_desc = description_entry.get()
        new_status = status_var.get()
        new_people = people_entry.get()
        if not new_name:
            messagebox.showerror("Error", "Name is required.")
            return
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""UPDATE assignments 
                     SET name=?, due_date=?, description=?, status=?, people_involved=? 
                     WHERE id=?""",
                  (new_name, new_due, new_desc, new_status, new_people, assignment[0]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Assignment updated!")
        win.destroy()
    #Submit button to update the assignment     
    Button(win, text="Submit", font=("Helvetica", 12), command=submit_edit).grid(row=5, column=0, columnspan=2, pady=10)

    # -------------------------------
    # Delete Assignment Button
    # -------------------------------
    def delete_assignment():
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this assignment?"):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("DELETE FROM assignments WHERE id=?", (assignment[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Assignment deleted successfully!")
            win.destroy()
    
    Button(win, text="Delete Assignment", font=("Helvetica", 12), fg="red", command=delete_assignment).grid(row=6, column=0, columnspan=2, pady=10)



# -------------------------------
# View All Assignments Window
# -------------------------------
def view_assignments_window(role):
    win = Toplevel(root)
    win.geometry("500x400")
    win.title("All Assignments")
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM assignments")
    assignments = c.fetchall()
    conn.close()
    
    if assignments:
        for assignment in assignments:
            assignment_str = f"{assignment[0]}: {assignment[1]}"
            # Use a lambda with default argument to capture the current assignment id
            Button(win, text=assignment_str, command=lambda a_id=assignment[0]: view_assignment_details(a_id, role)).pack(padx=10, pady=5)
    else:
        Label(win, text="No assignments found.", font=("Helvetica", 12)).pack(padx=10, pady=10)


# -------------------------------
# Main Application (Testing Area)
# -------------------------------
if __name__ == "__main__":
    root = Tk()
    root.title("Assignment Manager")
    root.geometry("500x400")
    
    initialize_db()  # Set up the database and table
    
    # For testing purposes, launch the Admin Interface.
    admin_interface()
    
    #Call the main loop for displaying the root window
    root.mainloop()
