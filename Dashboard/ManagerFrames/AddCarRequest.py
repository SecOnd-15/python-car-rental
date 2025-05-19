import tkinter as tk
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager

class AddCarRequestFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        
        self.configure(bg="#f0f0f0")
        
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        
        tk.Label(self, text="Add Car", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)

        form_frame.grid_rowconfigure(0, weight=1)
        form_frame.grid_rowconfigure(1, weight=1)
        form_frame.grid_rowconfigure(5, weight=1)
       
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
        form_frame.grid_columnconfigure(5, weight=1)

        self.car_make_label = tk.Label(form_frame, text="Car Maker:", bg="#f0f0f0", font=("Helvetica", 12))
        self.car_make_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.car_make_combobox = ttk.Combobox(form_frame, values=db_manager.Get.get_all_producer_names(cursor=db_manager.cursor), state="readonly", font=("Helvetica", 12))
        self.car_make_combobox.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        self.fuel_type_label = tk.Label(form_frame, text="Fuel Type:", bg="#f0f0f0", font=("Helvetica", 12))
        self.fuel_type_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.fuel_type_combobox = ttk.Combobox(form_frame, values=db_manager.Get.get_all_fuel_types(cursor=db_manager.cursor), state="readonly", font=("Helvetica", 12))
        self.fuel_type_combobox.grid(row=0, column=3, pady=5, padx=10, sticky="w")

        self.transmission_label = tk.Label(form_frame, text="Transmission:", bg="#f0f0f0", font=("Helvetica", 12))
        self.transmission_label.grid(row=0, column=4, padx=10, pady=5, sticky="e")
        self.transmission_combobox = ttk.Combobox(form_frame, values=db_manager.Get.get_all_transmission_types(cursor=db_manager.cursor), state="readonly", font=("Helvetica", 12))
        self.transmission_combobox.grid(row=0, column=5, pady=5, padx=10, sticky="w")

        self.car_year_label = tk.Label(form_frame, text="Car Year:", bg="#f0f0f0", font=("Helvetica", 12))
        self.car_year_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.car_year_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken")
        self.car_year_entry.grid(row=5, column=1, pady=5, padx=10, sticky="w")

        self.daily_rental_price_label = tk.Label(form_frame, text="Daily Rental Price (₱):", bg="#f0f0f0", font=("Helvetica", 12))
        self.daily_rental_price_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.daily_rental_price_entry = tk.Spinbox(form_frame, from_=0, to=10000, increment=0.5, format="%.2f", font=("Helvetica", 12), bd=0.5, relief="sunken")
        self.daily_rental_price_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.seats_label = tk.Label(form_frame, text="Seats:", bg="#f0f0f0", font=("Helvetica", 12))
        self.seats_label.grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.seats_spinbox = tk.Spinbox(form_frame, from_=1, to=10, font=("Helvetica", 12), bd=0.5, relief="sunken")
        self.seats_spinbox.grid(row=1, column=3, pady=5, padx=10, sticky="w")

        self.car_model_label = tk.Label(form_frame, text="Car Model:", bg="#f0f0f0", font=("Helvetica", 12))
        self.car_model_label.grid(row=1, column=4, padx=10, pady=5, sticky="e")
        self.car_model_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken")
        self.car_model_entry.grid(row=1, column=5, pady=5, padx=10, sticky="w")

        self.plate_number_label = tk.Label(form_frame, text="Plate Number:", bg="#f0f0f0", font=("Helvetica", 12))
        self.plate_number_label.grid(row=5, column=2, padx=10, pady=5, sticky="e")
        self.plate_number_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        self.plate_number_entry.grid(row=5, column=3, pady=5, padx=10, sticky="w")

        self.add_car_button = tk.Button(self, text="Add Car", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.car_button_functions)
        self.add_car_button.pack()


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
        self.tree.column("Deletion Status", width=100)

        
        self.load_data_from_db()

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 
        
       
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)


        self.pack(expand=True)

    def car_button_functions(self):
        car_make = self.car_make_combobox.get()
        car_model = self.car_model_entry.get()
        car_year = self.car_year_entry.get()
        fuel_type = self.fuel_type_combobox.get()
        transmission = self.transmission_combobox.get()
        daily_rental_price = self.daily_rental_price_entry.get()
        seats = self.seats_spinbox.get()
        plate_number = self.plate_number_entry.get()

        try:
            self.validation(car_make, car_model, car_year, daily_rental_price, seats, fuel_type, transmission, plate_number)

            db_manager.Insert.insert_car(
                cursor=db_manager.cursor, 
                conn=db_manager.conn, 
                car_make=car_make, 
                model_name=car_model, 
                car_year=car_year, 
                fuel_type=fuel_type, 
                transmission=transmission, 
                daily_rental_price=daily_rental_price, 
                seats=seats, 
                plate_number=plate_number
            )
            
            self.warningText.config(text="Successfully Added", fg="green")

            self.load_data_from_db()
           

        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")
            return

    
        
        self.clear()

    def validation(self, car_maker, car_model, car_year, daily_rental_price, seats, fuel_type, transmission, plate_number):
        if not car_maker.strip():
            raise ValueError("Car maker is required.")
        if not fuel_type.strip():
            raise ValueError("Fuel type is required.")
        if not transmission.strip():
            raise ValueError("Transmission is required.")

        try:
            price = float(daily_rental_price)
            if price <= 0:
                raise ValueError("Daily rental price must be greater than 0.00.")
        except ValueError:
            raise ValueError("Daily rental price must be a valid number.")

        if not daily_rental_price.strip():
            raise ValueError("Daily rental price is required.")
        if not seats.strip():
            raise ValueError("Seats are required.")
        if not car_model.strip():
            raise ValueError("Car model is required.")
        if not car_year.strip():
            raise ValueError("Car year is required.")
        if not car_year.isdigit():
            raise ValueError("Car year must be a numeric value.")
        if not plate_number.strip():
            raise ValueError("Plate number is required.")

        try:
            int(seats)
        except ValueError:
            raise ValueError("Seats must be an integer.")

    def clear(self):
        self.car_make_combobox.set('')
        self.car_model_entry.delete(0, tk.END)
        self.car_year_entry.delete(0, tk.END)
        self.fuel_type_combobox.set('')
        self.transmission_combobox.set('')
        self.daily_rental_price_entry.delete(0, tk.END)
        self.seats_spinbox.delete(0, "end")
        self.seats_spinbox.insert(0, "1")
        self.plate_number_entry.delete(0, tk.END)

    def load_data_from_db(self):
        start = self.start
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = db_manager.Get.get_all_cars_data(cursor=db_manager.cursor)

        for index, car in enumerate(data):
            if start > index:
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

    def block_scroll(self, event):
        return "break"