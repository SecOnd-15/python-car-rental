import tkinter as tk
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager

class AddServiceRequestFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        
        self.configure(bg="#f0f0f0")
        
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        tk.Label(self, text="Add Service", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Service Name:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.service_name_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken")
        self.service_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="Price (₱):", font=("Helvetica", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.price_entry = tk.Spinbox(form_frame, from_=0, to=10000, increment=0.5, format="%.2f", font=("Helvetica", 12), bd=0.5, relief="sunken", width=19)
        self.price_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.add_service_button = tk.Button(self, text="Add Service", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.service_button_functions)
        self.add_service_button.pack()


        self.pagination_frame = tk.Frame(self, bg="#f0f0f0")
        self.pagination_frame.pack()

        self.prev_button = tk.Button(
            self.pagination_frame,
            text="<< Previous",
            command=lambda: [setattr(self, 'start', max(0, self.start - 10)), self.load_data_from_db()]
        )
        self.prev_button.grid(row=0, column=0, padx=5)

        self.page_label = tk.Label(self.pagination_frame, text="", bg="#f0f0f0", font=("Helvetica", 10))
        self.page_label.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(
            self.pagination_frame,
            text="Next >>",
            command=lambda: [setattr(self, 'start', self.start + 10), self.load_data_from_db()]
        )

        self.next_button.grid(row=0, column=2, padx=5)

        self.tree = ttk.Treeview(self, columns=("Name", "Price", "Status"), show="headings")
        self.tree.heading("Name", text="Service Name")
        self.tree.heading("Price", text="Price (₱)")
        self.tree.heading("Status", text="Status")

        self.tree.column("Name", width=200)
        self.tree.column("Price", width=100)
        self.tree.column("Status", width=100)

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        

        self.load_data_from_db()
        self.pack(expand=True)

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll)

    def service_button_functions(self):
        name = self.service_name_entry.get()
        price = self.price_entry.get()

        try:
            self.validate(name, price)
            
            if (db_manager.Check.check_service_exists(cursor=db_manager.cursor, service_name=name)):
                raise ValueError(f"The service '{name}' already exists.")
            
          
            db_manager.Insert.insert_service(cursor=db_manager.cursor, conn=db_manager.conn, service_name=name, price=price)
            self.warningText.config(text="Successfully Added", fg="green")
            self.load_data_from_db()
        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")
            return

        self.clear()

    def validate(self, name, price):
        if not name.strip():
            raise ValueError("Service name is required.")

        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Price must be greater than 0.00.")
        except ValueError:
            raise ValueError("Price must be a valid number.")

    def clear(self):
        self.service_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, "0.00")

    
    def redirectInsert(self, name):
        self.service_name_entry.delete(0, tk.END)
        self.service_name_entry.insert(0, name)

    
    def load_data_from_db(self):
        
       
        self.tree.delete(*self.tree.get_children())
        
       
        data = db_manager.Get.get_all_services_data(cursor=db_manager.cursor)
        
    
        for index, service in enumerate(data):
            if self.start > index:
                continue
            self.tree.insert("", "end", values=(
                service['service_name'],  # Service Name
                service['price'],         # Price
                service['status_name']    # Status
            ))

    def block_scroll(self, event):
        return "break"