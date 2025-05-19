import tkinter as tk
from tkinter import ttk
import re
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager

class AddCustomerFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        
        self.configure(bg="#f0f0f0")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        tk.Label(self, text="Customer Management", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="First Name", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.first_name_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        tk.Label(form_frame, text="Last Name", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.last_name_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        tk.Label(form_frame, text="Email", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.email_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.email_entry.grid(row=3, column=0, padx=10, pady=2, sticky="w")

        tk.Label(form_frame, text="Phone Number", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=2, column=1, padx=5, pady=2, sticky="w")
        self.phone_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=2, sticky="w")

        tk.Label(form_frame, text="User License", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=4, column=1, padx=5, pady=2, sticky="w")
        self.user_license_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.user_license_entry.grid(row=5, column=1, padx=10, pady=2, sticky="w")
        
        tk.Label(form_frame, text="Address", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.address_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.address_entry.grid(row=5, column=0, padx=10, pady=2, sticky="w")

        self.add_customer_button = tk.Button(self, text="Add Customer", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.add_customer)
        self.add_customer_button.pack(pady=(20, 0))

        
        self.pagination_frame = tk.Frame(self, bg="#f0f0f0")
        self.pagination_frame.pack(pady=(5, 10))

        self.prev_button = tk.Button(
            self.pagination_frame,
            text="<< Previous",
            command=lambda: [setattr(self, 'start', max(0, self.start - 10)), self.load_customer_data()]
        )
        self.prev_button.grid(row=0, column=0, padx=5)

        self.page_label = tk.Label(self.pagination_frame, text="", bg="#f0f0f0", font=("Helvetica", 10))
        self.page_label.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(
            self.pagination_frame,
            text="Next >>",
            command=lambda: [setattr(self, 'start', self.start + 10), self.load_customer_data()]
        )

        self.next_button.grid(row=0, column=2, padx=5)


        self.tree = ttk.Treeview(
            self,
            columns=("First Name", "Last Name", "Email", "Phone", "Address", "License"),
            show="headings"
        )

        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone Number")
        self.tree.heading("Address", text="Address")
        self.tree.heading("License", text="License")

        for col in ("First Name", "Last Name", "Email", "Phone", "Address", "License"):
            self.tree.column(col, width=150)

        self.load_customer_data()

       
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 


       

    def load_customer_data(self):
        start = self.start

        for row in self.tree.get_children():
            self.tree.delete(row)
        customers = db_manager.Get.get_all_customers(cursor=db_manager.cursor)
        for index, customer in enumerate(customers):
            if start > index:
                continue
            self.tree.insert("", "end", values=(
                customer['first_name'],
                customer['last_name'],
                customer['email'],
                customer['phone_number'],
                customer['address'],
                customer['license']
            ))


    def validate(self):
        if not self.first_name_entry.get().strip():
            raise ValueError("First Name is required.")
        if not self.last_name_entry.get().strip():
            raise ValueError("Last Name is required.")
        if not self.user_license_entry.get().strip():
            raise ValueError("User License is required.")

        email = self.email_entry.get().strip()
        if not email:
            raise ValueError("Email is required.")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("Invalid email format.")
        if db_manager.Check.check_customer_if_exist(conn=db_manager.conn, cursor=db_manager.cursor, email=email):
            raise ValueError("Email already exists.")

        phone = self.phone_entry.get().strip()
        if not phone:
            raise ValueError("Phone Number is required.")
        if not phone.isdigit():
            raise ValueError("Phone Number must contain only digits.")

        if not self.address_entry.get().strip():
            raise ValueError("Address is required.")
        


    def add_customer(self):
        try:
            self.validate()


            first_name = self.first_name_entry.get().strip()
            last_name = self.last_name_entry.get().strip()
            email = self.email_entry.get().strip()
            phone_number = self.phone_entry.get().strip()
            address = self.address_entry.get().strip()
            user_license = self.user_license_entry.get().strip()

            db_manager.Insert.add_customer(
                conn=db_manager.conn,
                cursor=db_manager.cursor,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address,
                license=user_license
            )

            self.load_customer_data()

            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.address_entry.delete(0, tk.END)
            self.user_license_entry.delete(0, tk.END)

            self.warningText.config(text="Customer added successfully!", fg="green")

            self.load_customer_data()
            
        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")

    def block_scroll(self, event):
        return "break"