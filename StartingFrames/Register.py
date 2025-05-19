import tkinter as tk
from Database.DatabaseInstance import db_manager
import re

class RegisterFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg='white')

        # Title label
        self.label = tk.Label(self, text="Sign Up", bg='white', fg='black', font=('Arial', 30, 'bold'))
        self.label.pack(pady=50, padx=20, fill=tk.BOTH)

        # Warning text
        self.warning_text = tk.Label(self, text="", bg='white', fg='Red', font=('Arial', 10, 'bold'))
        self.warning_text.pack(pady=(0,1), padx=20, fill=tk.BOTH)

        self.firstName_label = tk.Label(self, text="First Name:", bg='white', fg='black', anchor='w')
        self.firstName_label.pack(padx=40,fill=tk.BOTH)
        self.firstName_entry = tk.Entry(self, bd=0.5, relief='solid', fg="#00998F")
        self.firstName_entry.pack(pady=(0, 5), padx=40, fill="x")

        self.lastName_label = tk.Label(self, text="Last Name:", bg='white', fg='black', anchor='w')
        self.lastName_label.pack(padx=40,fill=tk.BOTH)
        self.lastName_entry = tk.Entry(self, bd=0.5, relief='solid', fg="#00998F")
        self.lastName_entry.pack(pady=(0, 5), padx=40, fill="x")

        self.email_label = tk.Label(self, text="Email:", bg='white', fg='black', anchor='w')
        self.email_label.pack(padx=40,fill=tk.BOTH)
        self.email_entry = tk.Entry(self, bd=0.5, relief='solid', fg="#00998F")
        self.email_entry.pack(pady=(0, 5), padx=40, fill="x")

      
        self.password_label = tk.Label(self, text="Password:", bg='white', fg='black', anchor='w')
        self.password_label.pack(padx=40, fill=tk.BOTH)
        self.password_entry = tk.Entry(self, show="*", bd=0.5, relief='solid', fg="#00998F")  # Hide password input
        self.password_entry.pack(pady=(0, 10), padx=40, fill=tk.BOTH)

        # TODO: ADD FUNCTIONALITY
        self.register_button = tk.Button(self, bg="#00998F", fg="white", text="Register", relief="flat", command=self.Register) 
        self.register_button.pack(pady=(0,0), padx=40, expand=True, anchor='nw')


        self.login = tk.Label(self, text="Had an account already?", bg='white', fg='black', font=('Arial', 30, 'bold'))
        self.login.pack(side='left', pady=(0, 5), padx=(10, 0))
        
        self.login_button = tk.Button(self, bg="#00998F", fg="white", relief="flat", text="Login", command=lambda: app.ChangeFrame("LoginFrame"))
        self.login_button.pack(side='left', padx=(5, 0), pady=(0, 3))

        self.pack(expand=True, fill='both')

    def Register(self):
        try:
            # validate
            first_name, last_name, email, password = self.validate_fields()

            db_manager.Insert.add_user(
                conn=db_manager.conn,
                cursor=db_manager.cursor,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            # Clear
            self.firstName_entry.delete(0, tk.END)
            self.lastName_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.warning_text.config(text=str("Registration successful!"), fg='green')
        except ValueError as e:
            self.warning_text.config(text=str(e), fg='red')

    def validate_fields(self):
        # Check if empty
        first_name = self.firstName_entry.get().strip()
        last_name = self.lastName_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not first_name:
            raise ValueError("First name is required.")
        if not last_name:
            raise ValueError("Last name is required.")
        if not email:
            raise ValueError("Email is required.")
        if not password:
            raise ValueError("Password is required.")
        if db_manager.Check.check_user_if_exist(conn=db_manager.conn, cursor=db_manager.cursor,email=email):
            raise ValueError("Email already exist.")
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format.")
        
        return first_name, last_name, email, password

   
        


    def AdjustFontSize(self, size):
        size = max(10, min(size, 30))
        entry_size = max(8, int(size / 1.5)) 
        button_size = max(9, int(size / 1.3)) 

        for widget in self.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.config(font=('Arial', entry_size + 10))
            elif isinstance(widget, tk.Button):
                if widget.cget("text") == "Login":
                    widget.config(font=('Arial', int(button_size / 2)))
                    widget.config(width=size // 2)
                else:
                    widget.config(font=('Arial', button_size))
                    widget.config(width=size // 2)
            elif isinstance(widget, tk.Label):
                if widget.cget("text") == "Sign Up":
                    widget.config(font=('Arial', size + 10, 'bold'))
                else:
                    widget.config(font=('Arial', size - 10))