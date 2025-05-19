import tkinter as tk
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager

class EditCarRentalPriceFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        self.configure(bg="#f0f0f0")

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Edit Car Rental Price", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)

        self.plate_number_label = tk.Label(form_frame, text="Car Plate Number", bg="#f0f0f0", font=("Helvetica", 12))
        self.plate_number_label.grid(row=0, column=0, padx=5, sticky="w")

        plate_values = ["Select Plate"] + db_manager.Get.get_all_plate_numbers(cursor=db_manager.cursor)
        self.plate_number_combobox = ttk.Combobox(
            form_frame,
            values=plate_values,
            state="readonly",
            font=("Helvetica", 20)
        )
        self.plate_number_combobox.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.plate_number_combobox.current(0)
        self.plate_number_combobox.bind("<<ComboboxSelected>>", self.get_data)

        self.daily_rental_price = tk.Label(form_frame, text="New Price", bg="#f0f0f0", font=("Helvetica", 12))
        self.daily_rental_price.grid(row=2, column=0, padx=5, sticky="w")
        self.daily_rental_price_entry = tk.Spinbox(form_frame, from_=0, to=10000, increment=0.5, format="%.2f", font=("Helvetica", 20), bd=0.5, relief="sunken")
        self.daily_rental_price_entry.grid(row=3, column=0, pady=5, padx=10, sticky="w")

        self.edit_car_button = tk.Button(form_frame, text="Apply Price Change", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.applyEdit)
        self.edit_car_button.grid(row=6, column=0, pady=5, padx=10, sticky="ew")

        self.edit_car_button.bind("<Enter>", self.on_focus_out)

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

        self.tree = ttk.Treeview(self, columns=("Plate", "Make", "Model", "Year", "Fuel", "Trans", "Price", "Seats", "Availability", "Deletion Status"), show="headings")
        self.tree.heading("Plate", text="Plate Number")
        self.tree.heading("Make", text="Make")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Fuel", text="Fuel Type")
        self.tree.heading("Trans", text="Transmission")
        self.tree.heading("Price", text="Price (₱)")
        self.tree.heading("Seats", text="Seats")
        self.tree.heading("Availability", text="Availability")
        self.tree.heading("Deletion Status", text="Deletion Status")

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
        self.pack(expand=True)

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 

    def applyEdit(self):
        data = self.daily_rental_price_entry.get()
        licensePlate = self.plate_number_combobox.get().strip()
        try:
            self.validate(data)
            if not licensePlate or licensePlate == "Select Plate":
                raise ValueError("License plate is required.")
            db_manager.Edit.edit_car_price_by_plate(cursor=db_manager.cursor, conn=db_manager.conn, license_plate=licensePlate, new_price=data)

            self.warningText.config(text="Successfully edited price", fg="green")
            self.clear()
            self.load_data_from_db()
        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")

    def validate(self, daily_rental_price):
        if not daily_rental_price.strip():
            raise ValueError("Daily rental price is required.")
        try:
            price = float(daily_rental_price)
        except ValueError:
            raise ValueError("Daily rental price must be a valid number.")
        if price <= 0:
            raise ValueError("Daily rental price must be greater than 0.00.")

    def on_focus_out(self, event):
        data = self.daily_rental_price_entry.get().strip()
        try:
            number = float(data)
            formatted_price = f"{number:.2f}"
            self.daily_rental_price_entry.delete(0, tk.END)
            self.daily_rental_price_entry.insert(0, formatted_price)
        except ValueError:
            pass

    def clear(self):
        self.daily_rental_price_entry.delete(0, tk.END)
        self.plate_number_combobox.set("Select Plate")

    def load_data_from_db(self):
        self.tree.delete(*self.tree.get_children())
        
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
                car[6],  # Availability Status
                car[10]  # Deletion Status
            ))

    def get_data(self, event=None):
        selected_plate = self.plate_number_combobox.get().strip()
        if selected_plate == "Select Plate":
            self.load_data_from_db()
        else:
            for row in self.tree.get_children():
                self.tree.delete(row)
        
            data = db_manager.Get.get_car_data_by_license_plate(cursor=db_manager.cursor, license_plate=selected_plate)
            if data:
                self.tree.insert("", "end", values=(
                    data[9],  # Plate Number
                    data[1],  # Make (Producer Name)
                    data[2],  # Model
                    data[3],  # Year
                    data[4],  # Fuel Type
                    data[5],  # Transmission
                    data[7],  # Price
                    data[8],  # Seats
                    data[6],  # Availability Status
                    data[10]  # Deletion Status
                ))
            else:
                self.warningText.config(text="Car not found.", fg="red")

    def block_scroll(self, event):
        return "break"