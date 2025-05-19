import tkinter as tk
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager

class CarMaintenanceFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        
        self.configure(bg="#f0f0f0")

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        tk.Label(self, text="Car Maintenance", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)
        

        self.plate_number_label = tk.Label(form_frame, text="Car Plate Number", bg="#f0f0f0", font=("Helvetica", 12))
        self.plate_number_label.grid(row=0, column=0, padx=5, sticky="w")
        self.plate_number_combobox = ttk.Combobox(form_frame, values=["Select Plate"] + db_manager.Get.get_all_license_plates_for_available_or_maintenance(cursor=db_manager.cursor), state="readonly", font=("Helvetica", 20))
        self.plate_number_combobox.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        self.availability_car_button = tk.Button(form_frame, text="Toggle Availability", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.toggle_availability)
        self.availability_car_button.grid(row=5, column=0, pady=5, padx=10, sticky="ew")


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


        self.tree = ttk.Treeview(self, columns=("Plate", "Make", "Model", "Year", "Fuel", "Trans", "Price", "Seats", "Availability"), show="headings")
        self.tree.heading("Plate", text="Plate Number")
        self.tree.heading("Make", text="Make")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Fuel", text="Fuel Type")
        self.tree.heading("Trans", text="Transmission")
        self.tree.heading("Price", text="Price (₱)")
        self.tree.heading("Seats", text="Seats")
        self.tree.heading("Availability", text="Availability")

        self.tree.column("Plate", width=100)
        self.tree.column("Make", width=100)
        self.tree.column("Model", width=100)
        self.tree.column("Year", width=100)
        self.tree.column("Fuel", width=100)
        self.tree.column("Trans", width=100)
        self.tree.column("Price", width=100)
        self.tree.column("Seats", width=100)
        self.tree.column("Availability", width=100)

        self.load_data_from_db()

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

      
        self.plate_number_combobox.bind("<Enter>", self.check_new_car_update_on_focus_in)
        self.plate_number_combobox.bind("<<ComboboxSelected>>", self.get_car_data)

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 

    def toggle_availability(self):
        licensePlate = self.plate_number_combobox.get()
        
        try:
            if not licensePlate.strip():
                raise ValueError("License plate is required.")
            
        
            selected_item = self.tree.selection()
            if selected_item:
                selected_item = selected_item[0] 
            
         
            current_status = db_manager.Get.get_car_availability_by_plate(cursor=db_manager.cursor, license_plate=licensePlate)
            if current_status == "Maintenance":
                new_status = "Available"
            else:
                new_status = "Maintenance"
            
            db_manager.Edit.edit_car_availability(cursor=db_manager.cursor, conn=db_manager.conn, newStatus=new_status, licensePlate=licensePlate)
            
  
            self.get_car_data(None) 
            
       
            if selected_item:
                self.tree.selection_set(selected_item) 

          
            self.warningText.config(text=f"Successfully changed car status to {new_status}", fg="green")
            
         
            self.clear()

        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")
            return

    def check_new_car_update_on_focus_in(self, event):
        self.plate_number_combobox.config(values=["Select Plate"] + db_manager.Get.get_all_license_plates_for_available_or_maintenance(cursor=db_manager.cursor), state="readonly", font=("Helvetica", 20))

    def get_car_data(self, event):
        selected_plate = self.plate_number_combobox.get()
        if selected_plate == "Select Plate":
            self.load_data_from_db()
        else:
            self.load_data_by_plate(selected_plate)

    def load_data_from_db(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        
        data = db_manager.Get.get_all_cars_data(cursor=db_manager.cursor)

        for index, car in enumerate(data):
            if self.start > index:
                continue
            
            self.tree.insert("", "end", values=(
                car[9],  # Plate Number
                car[1],  # Make (Producer Name)
                car[2],  # Model
                car[3],  # Year
                car[4],  # Fuel Type
                car[5],  # Transmission
                car[7],  # Price
                car[8],  # Seats
                car[6]   # Availability Status
            ))

    def load_data_by_plate(self, license_plate):
        for row in self.tree.get_children():
            self.tree.delete(row)

        car = db_manager.Get.get_car_data_by_license_plate(cursor=db_manager.cursor, license_plate=license_plate)

        if car:
            self.tree.insert("", "end", values=(
                car[9],  # Plate Number
                car[1],  # Make (Producer Name)
                car[2],  # Model
                car[3],  # Year
                car[4],  # Fuel Type
                car[5],  # Transmission
                car[7],  # Price
                car[8],  # Seats
                car[6]   # Availability Status
            ))

    def clear(self):
        pass
        #self.plate_number_combobox.set('')


    def block_scroll(self, event):
        return "break"
