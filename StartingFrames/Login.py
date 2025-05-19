import tkinter as tk
from Database.DatabaseInstance import db_manager


class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg='white')

        self.app = app

        # Title label
        self.label = tk.Label(self, text="LOG IN", bg='white', fg='#00998F', font=('Arial', 30, 'bold'))
        self.label.pack(pady=50, padx=20, fill=tk.BOTH)

        # Warning text
        self.warning_text = tk.Label(self, text="", bg='white', fg='Red', font=('Arial', 10, 'bold'))
        self.warning_text.pack(pady=(0,1), padx=20, fill=tk.BOTH)


        # Email Label and Entry
        self.email_label = tk.Label(self, text="Email:", bg='white', fg='black', anchor='w')
        self.email_label.pack(padx=40,fill=tk.BOTH)
        self.email_entry = tk.Entry(self, bd=0.5, relief='solid', fg="#00998F")
        self.email_entry.pack(pady=(0, 5), padx=40, fill="x")

        # Password Label and Entry
        self.password_label = tk.Label(self, text="Password:", bg='white', fg='black', anchor='w')
        self.password_label.pack(padx=40, fill=tk.BOTH)
        self.password_entry = tk.Entry(self, show="*", bd=0.5, relief='solid', fg="#00998F")
        self.password_entry.pack(pady=(0, 10), padx=40, fill=tk.BOTH)

        
        self.login_button = tk.Button(self, bg="#00998F", fg="white", text="Login", relief="flat", command=self.Login)
        self.login_button.pack(pady=(0,0), padx=40, expand=True, anchor='nw')


        self.register = tk.Label(self, text="I don't have an account", bg='white', fg='black', font=('Arial', 30, 'bold'))
        self.register.pack(side='left', pady=(0, 5), padx=(10, 0))
       
        self.register_button = tk.Button(self, bg="#00998F", fg="white", relief="flat", text="Register", command=lambda: app.ChangeFrame("RegisterFrame"))
        self.register_button.pack(side='left', padx=(5, 0), pady=(0, 3))


        
        self.pack(expand=True, fill='both')

    def Login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if (db_manager.Check.check_of_credentials_match(cursor=db_manager.cursor, conn=db_manager.conn, email=email, password=password)):
            self.app.GoToDashboard(email=email, password=password)
        else:
            self.warning_text.config(text="User doesn't exist", fg='red')


    def AdjustFontSize(self, size):
        size = max(10, min(size, 30))
        entry_size = max(8, int(size / 1.5)) 
        button_size = max(9, int(size / 1.3)) 

        for widget in self.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.config(font=('Arial', entry_size + 10))
            elif isinstance(widget, tk.Button):
                if widget.cget("text") == "Register":
                    widget.config(font=('Arial', int(button_size / 2)))
                    widget.config(width=size // 2)
                else:
                    widget.config(font=('Arial', button_size))
                    widget.config(width=size // 2)
            elif isinstance(widget, tk.Label):
                if widget.cget("text") == "LOG IN":
                    widget.config(font=('Arial', size + 10, 'bold'))
                else:
                    widget.config(font=('Arial', size - 10))

       