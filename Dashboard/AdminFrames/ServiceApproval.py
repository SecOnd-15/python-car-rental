import tkinter as tk
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager

class ServiceApprovalFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        
        self.configure(bg="#f0f0f0")

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        tk.Label(self, text="Approve Services", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)

        self.service_name_label = tk.Label(form_frame, text="Select Service to Approve", bg="#f0f0f0", font=("Helvetica", 12))
        self.service_name_label.grid(row=0, column=0, padx=5, sticky="w")

        
        service_names = db_manager.Get.get_all_pending_service_names(cursor=db_manager.cursor)
        self.service_name_combobox = ttk.Combobox(form_frame, values=service_names, state="readonly", font=("Helvetica", 20))
        self.service_name_combobox.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        self.approve_service_button = tk.Button(form_frame, text="Approve Service", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.approve_service)
        self.approve_service_button.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

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
       
        self.tree = ttk.Treeview(self, columns=("Service", "Price", "Status"), show="headings")
        self.tree.heading("Service", text="Service Name", anchor="w")
        self.tree.heading("Price", text="Price (₱)", anchor="w")
        self.tree.heading("Status", text="Status", anchor="w")

       
        for col in self.tree["columns"]:
            self.tree.column(col, width=150, anchor="w")

     
        self.load_data_from_db()

     
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

       
        self.service_name_combobox.bind("<Enter>", self.refresh_service_list)

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 

    def approve_service(self):
        service_name = self.service_name_combobox.get()
        try:
            if not service_name.strip():
                raise ValueError("Service name is required.")
            
         
            db_manager.Edit.edit_service_to_available(cursor=db_manager.cursor, conn=db_manager.conn, service_name=service_name)
            self.warningText.config(text="Successfully approved service.", fg="green")
            self.clear()
            self.load_data_from_db()  # Refresh the data
        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")

    def refresh_service_list(self, event):
       
        service_names = db_manager.Get.get_all_pending_service_names(cursor=db_manager.cursor)
        self.service_name_combobox.config(values=service_names)

    def load_data_from_db(self):
     
        for row in self.tree.get_children():
            self.tree.delete(row)

     
        data = db_manager.Get.get_all_pending_services(cursor=db_manager.cursor)

      
        for index, service in enumerate(data):
            if self.start > index:
                continue
            self.tree.insert("", "end", values=(service['service_name'], service['price'], service['status_name']))

    def clear(self):
     
        self.service_name_combobox.set('')

    def block_scroll(self, event):
        return "break"




