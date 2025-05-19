import tkinter as tk
import re
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry

class RentCarFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        
        self.configure(bg="#f0f0f0")
        self.total_price = 0
        self.base_price = 0
        self.selected_services = []
        
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        tk.Label(self, text="Rent a Car", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack()
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 0))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=(0, 0))

        self.car_plate_label = tk.Label(form_frame, text="Car Plate Number:", bg="#f0f0f0", font=("Helvetica", 12))
        self.car_plate_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.car_plate_combobox = ttk.Combobox(form_frame, values=["Select plate"] + db_manager.Get.get_all_available_license_plate(cursor=db_manager.cursor), state="readonly", font=("Helvetica", 12))
        self.car_plate_combobox.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        self.car_plate_combobox.bind("<<ComboboxSelected>>", self.on_plate_selected)


        
        self.renter_name_label = tk.Label(form_frame, text="Renter's Full Name:", bg="#f0f0f0", font=("Helvetica", 12))
        self.renter_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.customer_emails = db_manager.Get.get_all_customer_emails(cursor=db_manager.cursor)

        self.renter_email_var = tk.StringVar()
        self.renter_email_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.renter_email_var,
            font=("Helvetica", 12),
            state="readonly"
        )
        self.renter_email_combobox['values'] = self.customer_emails
        self.renter_email_combobox.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.payment_method_label = tk.Label(form_frame, text="Payment Method:", bg="#f0f0f0", font=("Helvetica", 12))
        self.payment_method_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.payment_method_combobox = ttk.Combobox(form_frame, values=["Down Payment", "Cash in Direct"], state="readonly", font=("Helvetica", 12))
        self.payment_method_combobox.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        self.payment_method_combobox.bind("<<ComboboxSelected>>", self.toggle_downpayment_spinbox)


        self.downpayment_label = tk.Label(form_frame, text="Down Payment Amount (₱):", bg="#f0f0f0", font=("Helvetica", 12))
        self.downpayment_spinbox = tk.Spinbox(form_frame, from_=0, to=10000, increment=50, font=("Helvetica", 12), state="disabled")
        self.downpayment_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.downpayment_spinbox.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        self.rental_period_label = tk.Label(form_frame, text="Rental Period (Days):", bg="#f0f0f0", font=("Helvetica", 12))
        self.rental_period_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.rental_period_var = tk.StringVar()
        self.rental_period_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken", state="readonly", textvariable=self.rental_period_var)
        self.rental_period_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        self.start_date_label = tk.Label(form_frame, text="Start Date (DD/MM/YY):",
                                 bg="#f0f0f0", font=("Helvetica", 12))
        self.start_date_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.start_date_entry = DateEntry(form_frame,
                                        font=("Helvetica", 12),
                                        date_pattern='dd/MM/yy',
                                        background='white',
                                        foreground='black',
                                        borderwidth=0.5,
                                        relief="sunken",
                                        width=20)
        self.start_date_entry.grid(row=5, column=1, pady=5, padx=10, sticky="w")
        self.start_date_entry.bind("<FocusOut>", self.calculate_total_price)
        self.start_date_entry.bind("<KeyRelease>", self.calculate_total_price)
        self.start_date_entry.bind("<<DateEntrySelected>>", self.calculate_total_price)

        self.end_date_label = tk.Label(form_frame, text="End Date (DD/MM/YY):",
                                    bg="#f0f0f0", font=("Helvetica", 12))
        self.end_date_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")

        self.end_date_entry = DateEntry(form_frame,
                                        font=("Helvetica", 12),
                                        date_pattern='dd/MM/yy',
                                        background='white',
                                        foreground='black',
                                        borderwidth=0.5,
                                        relief="sunken",
                                        width=20)
        self.end_date_entry.grid(row=6, column=1, pady=5, padx=10, sticky="w")
        self.end_date_entry.bind("<FocusOut>", self.calculate_total_price)
        self.end_date_entry.bind("<KeyRelease>", self.calculate_total_price)
        self.end_date_entry.bind("<<DateEntrySelected>>", self.calculate_total_price)

        self.total_price_label = tk.Label(form_frame, text="Preliminary Total (₱):", bg="#f0f0f0", font=("Helvetica", 12))
        self.total_price_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.total_price_var = tk.StringVar()
        self.total_price_var.set(f"₱{self.total_price:.2f}")
        self.total_price_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken", state="readonly", textvariable=self.total_price_var)
        self.total_price_entry.grid(row=7, column=1, pady=5, padx=10, sticky="w")
        

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

        services_container = tk.Frame(form_frame, bg="#e0e0e0")
        services_container.grid(row=0, column=2, rowspan=6, padx=10, pady=5, sticky="nsew")

        services_canvas = tk.Canvas(services_container, bg="#e0e0e0", highlightthickness=0)
        services_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(services_container, orient="vertical", command=services_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        services_canvas.configure(yscrollcommand=scrollbar.set)

        self.services_frame = tk.Frame(services_canvas, bg="#e0e0e0")
        services_canvas.create_window((0, 0), window=self.services_frame, anchor="nw")

        services_title = tk.Label(self.services_frame, text="Additional Services:", bg="#e0e0e0", font=("Helvetica", 12, "bold"))
        services_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        service_data = db_manager.Get.get_all_service_names_and_prices(cursor=db_manager.cursor)

        self.service_vars = {}

       

        # Services
        for i, (service, price) in enumerate(service_data.items()):
            label = tk.Label(self.services_frame, text=f"{service} (₱{price:.2f}):", bg="#e0e0e0", font=("Helvetica", 11))
            label.grid(row=i + 1, column=0, sticky="w", pady=2)

            var = tk.IntVar(value=0)
            self.service_vars[service] = var

            rb_no = tk.Radiobutton(
                self.services_frame, text="No", variable=var, value=0,
                bg="#e0e0e0", font=("Helvetica", 10), command=self.update_selected_services
            )
            rb_no.grid(row=i + 1, column=1, sticky="w", padx=(10, 0))

            rb_yes = tk.Radiobutton(
                self.services_frame, text="Yes", variable=var, value=1,
                bg="#e0e0e0", font=("Helvetica", 10), command=self.update_selected_services
            )
            rb_yes.grid(row=i + 1, column=2, sticky="w")

        self.rent_car_button = tk.Button(self, text="Rent Car", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.rent_car_button)
        self.rent_car_button.pack(pady=(0, 0))
        
        # Car Tree
        self.tree = ttk.Treeview(self, columns=("Plate", "Make", "Model", "Year", "Fuel", "Trans", "Price", "Seats", "Availability"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.load_data_from_db()

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 

    def toggle_downpayment_spinbox(self, event=None):
        if self.payment_method_combobox.get() == "Down Payment":
            self.downpayment_spinbox.config(state="normal")
        else:
            self.downpayment_spinbox.config(state="disabled")

    def update_selected_services(self):
        self.selected_services = [
            service for service, var in self.service_vars.items() if var.get() == 1
        ]
        self.calculate_total_price()

    def on_plate_selected(self, event=None):
       

        selected_plate = self.car_plate_combobox.get()

        if selected_plate == "Select plate":
            self.load_data_from_db()
            return



        # First show the selected car's details
        self.show_selected_plate_data(event)
        
        # Then calculate the total price
        self.calculate_total_price(event)

    def show_selected_plate_data(self, event=None):
        selected_plate = self.car_plate_combobox.get()
        self.tree.delete(*self.tree.get_children())
        if selected_plate == "Select Plate Number":
            self.load_data_from_db()
        else:
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

    def load_data_from_db(self):
        start = self.start
        self.tree.delete(*self.tree.get_children())
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

    def calculate_total_price(self, event=None):
        # Get the car's base price
        plate_number = self.car_plate_combobox.get()
        price = db_manager.Get.get_car_price_by_plate(cursor=db_manager.cursor, plate_number=plate_number)
        
        # Check if a valid price was retrieved
        if price is not None:
            self.base_price = price
            
            # Get the rental period start and end dates
            start_date_str = self.start_date_entry.get()
            end_date_str = self.end_date_entry.get()
            
            # if missing and isa sa start or end date, then default price 0
            if not start_date_str or not end_date_str:
                self.total_price = 0
                self.total_price_var.set(f"₱{self.total_price:.2f}")
                return
            
            try:
                start_date = datetime.strptime(start_date_str, "%d/%m/%y")
                end_date = datetime.strptime(end_date_str, "%d/%m/%y")
                rental_period = (end_date - start_date).days
                
                # If same day and end considered giyapon day 1
                if rental_period <= 0:
                    rental_period = 1
                    self.total_price = self.base_price
                    self.rental_period_var.set(str(rental_period))
                else:
                    self.rental_period_var.set(str(rental_period))
                    self.total_price = self.base_price * rental_period

               
            except ValueError:
                self.total_price = 0 
        
            # Add prices for selected services
            for service, var in self.service_vars.items():
                if var.get() == 1:
                    service_price = db_manager.Get.get_service_price_by_name(cursor=db_manager.cursor, service_name=service)
                    if service_price:
                        self.total_price += service_price

            # Update the total price field
            self.total_price_var.set(f"₱{self.total_price:.2f}")

    def validate_rent_inputs(self):
        plate = self.car_plate_combobox.get().strip()
        renter = self.renter_email_combobox.get().strip()
        start_date_str = self.start_date_entry.get().strip()
        end_date_str = self.end_date_entry.get().strip()
        payment = self.payment_method_combobox.get().strip()

        if not plate:
            raise ValueError("Car plate number is required.")
        
        if not renter:
            raise ValueError("Renter's email is required.")
        
        if not start_date_str:
            raise ValueError("Start date is required.")
        
        if not end_date_str:
            raise ValueError("End date is required.")

        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%y")
        except ValueError:
            raise ValueError("Start date must be in DD/MM/YY format.")

        try:
            end_date = datetime.strptime(end_date_str, "%d/%m/%y")
        except ValueError:
            raise ValueError("End date must be in DD/MM/YY format.")

        if end_date < start_date:
            raise ValueError("End date cannot be before start date.")
        
        if not payment:
            raise ValueError("Payment method is required.")

    def rent_car_button(self):
        try:
            self.validate_rent_inputs()

            customer_email = self.renter_email_combobox.get().strip()
            car_plate = self.car_plate_combobox.get().strip()

            # Optional: reputation check
            reputation = db_manager.Get.get_user_reputation_by_email(cursor=db_manager.cursor, email=customer_email)
            if reputation is not None and reputation < 20:
                response = messagebox.askyesno("Bad Reputation Warning",
                                            "This customer has a bad reputation (below 20). Do you still want to proceed?")
                if not response:
                    return

            rental_date = self.start_date_entry.get().strip()
            return_date = self.end_date_entry.get().strip()
            total_amount = float(re.sub(r'[^\d.]', '', self.total_price_entry.get()))

            payment_method = self.payment_method_combobox.get().strip()
            downpayment_amount = float(self.downpayment_spinbox.get()) if payment_method == "Down Payment" else 0.0

            selected_services = [
                service for service, var in self.service_vars.items() if var.get() == 1
            ]

            db_manager.Insert.add_rental(
                conn=db_manager.conn,
                cursor=db_manager.cursor,
                customer_email=customer_email,
                plate_number=car_plate,
                rental_date=rental_date,
                return_date=return_date,
                total_amount=total_amount,
                downpayment_amount=downpayment_amount,
                selected_services=selected_services
            )

            db_manager.Edit.edit_car_availability(
                cursor=db_manager.cursor,
                conn=db_manager.conn,
                licensePlate=car_plate,
                newStatus="Unavailable"
            )

            self.warningText.config(text="Successful Rent!", fg="green")
            self.clear()

            self.car_plate_combobox["values"] = ["Select plate"] + db_manager.Get.get_all_available_license_plate(cursor=db_manager.cursor)
       
        
            

        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")

    def refresh(self):
        self.renter_email_combobox['values'] = db_manager.Get.get_all_customer_emails(cursor=db_manager.cursor)


    def clear(self):
        self.car_plate_combobox.set('')
        self.renter_email_combobox.set('')

        for entry in [self.start_date_entry, self.end_date_entry]:
            entry.delete(0, tk.END)

        self.payment_method_combobox.set('')
        self.downpayment_spinbox.configure(state="disabled")

        self.total_price = 0
        self.total_price_var.set(f"₱{self.total_price:.2f}")

        for var in self.service_vars.values():
            var.set(0)

        self.warningText.config(text="")
        self.rental_period_var.set('')

    def block_scroll(self, event):
        return "break"