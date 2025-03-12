import sqlite3
from tkinter import *
from tkinter import messagebox

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


#Call the main loop for displaying the root window
root.mainloop()

