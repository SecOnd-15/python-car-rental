import tkinter as tk
from tkinter import ttk, messagebox
from Database.DatabaseInstance import db_manager
from decimal import Decimal
from datetime import datetime
from tkcalendar import DateEntry
import os

class ReturnRentFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        self.configure(bg="#f0f0f0")
        self.total_price = 0
        self.selected_damages = []
        self.user_score_penalty = 0
        # Adjust ra diri kung pila ang penalty ninyo
        self.car_penalty_cost = 500
        self.rent_overdue_multiplier = 5
        self.rent_damage_multiplier = 4

        tk.Label(self, text="Return Rental", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=10)

        self.rent_id_label = tk.Label(form_frame, text="Rent ID:", bg="#f0f0f0", font=("Helvetica", 12))
        self.rent_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.rent_id_combobox = ttk.Combobox(
            form_frame,
            values=["Select Rent ID"] + db_manager.Get.all_ongoing_rental_ids(cursor=db_manager.cursor),
            state="readonly",
            font=("Helvetica", 12)
        )
        self.rent_id_combobox.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        self.rent_id_combobox.bind("<<ComboboxSelected>>", self.on_plate_selected)

        self.return_date_label = tk.Label(form_frame, text="Return Date (DD/MM/YY):",
                                 bg="#f0f0f0", font=("Helvetica", 12))
        self.return_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.return_date_entry = DateEntry(form_frame,
                                        font=("Helvetica", 12),
                                        date_pattern='dd/MM/yy',
                                        background='white',
                                        foreground='black',
                                        borderwidth=0.5,
                                        relief="sunken",
                                        width=20)
        self.return_date_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

       
        self.return_date_entry.bind("<KeyRelease>", self.on_date_type)

       
        self.return_date_entry.bind("<<DateEntrySelected>>", self.on_date_type)

        self.overdue_days_label = tk.Label(form_frame, text="Overdue Days:", bg="#f0f0f0", font=("Helvetica", 12))
        self.overdue_days_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.overdue_days_var = tk.StringVar()
        self.overdue_days_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken", state="readonly", textvariable=self.overdue_days_var)
        self.overdue_days_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.total_price_label = tk.Label(form_frame, text="Total Price (₱):", bg="#f0f0f0", font=("Helvetica", 12))
        self.total_price_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.total_price_var = tk.StringVar()
        self.total_price_var.set(f"₱{self.total_price:.2f}")
        self.total_price_entry = tk.Entry(form_frame, font=("Helvetica", 12), bd=0.5, relief="sunken", state="readonly", textvariable=self.total_price_var)
        self.total_price_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        damage_container = tk.Frame(form_frame, bg="#e0e0e0")
        damage_container.grid(row=0, column=2, rowspan=6, padx=10, pady=5, sticky="nsew")

        damage_canvas = tk.Canvas(damage_container, bg="#e0e0e0", highlightthickness=0)
        damage_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(damage_container, orient="vertical", command=damage_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        damage_canvas.configure(yscrollcommand=scrollbar.set)

        self.damage_frame = tk.Frame(damage_canvas, bg="#e0e0e0")
        damage_canvas.create_window((0, 0), window=self.damage_frame, anchor="nw")

        self.damage_frame.bind("<Configure>", lambda e: damage_canvas.configure(scrollregion=damage_canvas.bbox("all")))

        damage_title = tk.Label(self.damage_frame, text="Reported Damages:", bg="#e0e0e0", font=("Helvetica", 12, "bold"))
        damage_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        self.damage_data = {
            "Scratch": 50.00,
            "Dented Bumper": 100.00,
            "Broken Mirror": 75.00,
            "Flat Tire": 30.00,
            "Windshield Crack": 120.00,
            "Broken Headlight": 90.00,
            "Broken Taillight": 70.00,
            "Stained Upholstery": 60.00,
            "Torn Seat Fabric": 80.00,
            "Missing Floor Mat": 20.00,
            "Dead Battery": 110.00,
            "Engine Trouble": 300.00,
            "Transmission Issue": 400.00,
            "Broken AC": 150.00,
            "Damaged Paint": 200.00,
            "Lost Key": 100.00,
            "Broken Door Handle": 60.00,
            "Bent Rim": 90.00,
            "Oil Leak": 120.00,
            "Damaged Undercarriage": 250.00,
            "Broken Radio": 70.00,
            "Cracked Dashboard": 130.00,
            "Broken GPS Screen": 180.00,
            "Malfunctioning Wipers": 25.00,
            "Broken Side Window": 110.00
        }

        self.damage_vars = {}

        for i, (damage, price) in enumerate(self.damage_data.items()):
            label = tk.Label(self.damage_frame, text=f"{damage} (₱{price:.2f}):", bg="#e0e0e0", font=("Helvetica", 11))
            label.grid(row=i + 1, column=0, sticky="w", pady=2)

            var = tk.IntVar(value=0)
            self.damage_vars[damage] = var

            rb_no = tk.Radiobutton(
                self.damage_frame, text="No", variable=var, value=0, command=self.update_selected_damages,
                bg="#e0e0e0", font=("Helvetica", 10)
            )
            rb_no.grid(row=i + 1, column=1, sticky="w", padx=(10, 0))

            rb_yes = tk.Radiobutton(
                self.damage_frame, text="Yes", variable=var, value=1, command=self.update_selected_damages,
                bg="#e0e0e0", font=("Helvetica", 10)
            )
            rb_yes.grid(row=i + 1, column=2, sticky="w")

        self.return_button = tk.Button(self, text="Mark as Returned", font=("Helvetica", 14), bg="#00998F",bd=0, fg="white", command=self.edit_button_pressed)
        self.return_button.pack(pady=10)

        self.pagination_frame = tk.Frame(self, bg="#f0f0f0")
        self.pagination_frame.pack(pady=(5, 10))

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


        self.tree = ttk.Treeview(self, columns=("id", "plate", "start_date", "end_date", "preliminary_total", "status"), show="headings")

        self.tree.heading("id", text="Rental ID")
        self.tree.heading("plate", text="Plate Number")
        self.tree.heading("start_date", text="Rental Date")
        self.tree.heading("end_date", text="Return Date")
        self.tree.heading("preliminary_total", text="Preliminary Total")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=100)
        self.tree.column("plate", width=140)
        self.tree.column("start_date", width=140)
        self.tree.column("end_date", width=140)
        self.tree.column("preliminary_total", width=140)
        self.tree.column("status", width=140)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_data_from_db()

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 

    def edit_button_pressed(self):
        try:
            self.validate_rent_inputs()
            self.receipt_maker()
            customer_id = db_manager.Get.get_customer_id_by_rent_id(conn=db_manager.conn, cursor=db_manager.cursor,rent_id=self.rent_id_combobox.get().strip())
            db_manager.Edit.edit_customer_reputation(conn=db_manager.conn, cursor=db_manager.cursor,customer_id=customer_id ,reputation_to_add=self.user_score_penalty)

            db_manager.Edit.edit_rental_as_returned(conn=db_manager.conn, cursor=db_manager.cursor,rent_id=self.rent_id_combobox.get().strip())
            db_manager.Edit.edit_car_availability_to_available(conn=db_manager.conn, cursor=db_manager.cursor,rent_id=self.rent_id_combobox.get().strip())

            self.warningText.config(
                text="Rental successful! Please check your receipt on the desktop.",
                fg="green"
            )

            db_manager.Edit.update_total_amount(cursor=db_manager.cursor, rental_id=self.rent_id_combobox.get().strip(), new_total_amount=self.total_price)

            self.clear()
        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")

    def receipt_maker(self):
        rent_id = self.rent_id_combobox.get().strip()

        full_name = db_manager.Get.get_customer_full_name_by_rent_id(conn=db_manager.conn, cursor=db_manager.cursor, rent_id=rent_id)
        starting_date = db_manager.Get.get_rental_date(cursor=db_manager.cursor, rental_id=rent_id)
        return_date = self.return_date_entry.get().strip()

        start_date = datetime.strptime(starting_date, "%d/%m/%y")
        end_date = datetime.strptime(return_date, "%d/%m/%y")

        days_rented = (end_date - start_date).days

        services = db_manager.Get.get_services_by_rent_id_with_price(conn=db_manager.conn, cursor=db_manager.cursor, rent_id=rent_id)

        downpayment = float(db_manager.Get.get_downpayment_by_rent_id(conn=db_manager.conn, cursor=db_manager.cursor, rent_id=rent_id))
        total = float(self.total_price)
        
        

        # Create the receipt content as a string
        receipt_content = f"""        RENTAL RECEIPT
        ----------------------------------------
        Customer: {full_name}
        Car Plate: {rent_id}
        Starting Date: {starting_date}
        Return Date: {return_date}
        Days Rented: {days_rented}
        Days Overdue: {self.overdue_days_var.get().strip()}
        Downpayment: ₱{downpayment:.2f}
        Total Price: ₱{total:.2f}
        ----------------------------------------\n
        """
        if self.selected_damages:
            receipt_content += "Damage Charges:\n" 
            for damage in self.selected_damages:
                if damage in self.damage_data:
                    receipt_content += f"         - {damage}: ₱{self.damage_data[damage]:.2f}\n"  

      
        if services:
            if self.selected_damages:
                receipt_content += "        Additional Services:\n" 
            else:
                receipt_content += "Additional Services:\n" 
            for service, cost in services:
                receipt_content += f"         - {service}: ₱{cost:.2f}\n" 

       
        total_after_downpayment = total - downpayment

        receipt_content += f"""
        ----------------------------------------
        TOTAL AMOUNT DUE:         ₱{total:.2f}
        Amount After Downpayment: ₱{total_after_downpayment:.2f}
        ----------------------------------------
        Thank you for choosing our service!
        """

       
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        receipt_filename = f"Receipt_rent_{rent_id}.txt"
        receipt_path = os.path.join(desktop_path, receipt_filename)

        
        with open(receipt_path, 'w', encoding='utf-8') as file:
            file.write(receipt_content)

        print(f"Receipt saved to: {receipt_path}")


    def validate_rent_inputs(self):
        rent_id = self.rent_id_combobox.get().strip()
        return_date_str = self.return_date_entry.get().strip()
        total_price_str = self.total_price_var.get().strip()

        if rent_id == "Select Rent ID" or not rent_id:
            raise ValueError("Rent ID is required.")

        if not return_date_str:
            raise ValueError("Return date is required.")
        
        try:
            return_date = datetime.strptime(return_date_str, "%d/%m/%y")
        except ValueError:
            raise ValueError("Return date must be in DD/MM/YY format.")
        
        
        if not total_price_str.startswith("₱"):
            raise ValueError("Total price is not set correctly.")
        
        try:
            total_price = float(total_price_str.strip("₱"))
        except ValueError:
            raise ValueError("Total price must be a valid number.")

        if total_price < 0:
            raise ValueError("Total price cannot be negative.")



    def on_date_type(self, event=None):
        self.calculate_total()

    def calculate_total(self):
        selected_id = self.rent_id_combobox.get()
        if selected_id != "Select Rent ID":
            rental_data = db_manager.Get.get_ongoing_rental_by_id(cursor=db_manager.cursor, rental_id=selected_id)
            preliminary_total = rental_data[4]

            total_damage_cost = Decimal(self.calculate_damage_cost())
            penalty = self.calculate_date_punishment()

            final_total = float(preliminary_total) + float(total_damage_cost) + float(penalty)
            self.set_total_price(final_total)

    def update_selected_damages(self):
        self.selected_damages = [
            damage for damage, var in self.damage_vars.items() if var.get() == 1
        ]
        self.calculate_total()

    def calculate_damage_cost(self):
        total_damage = 0
        for damage, price in self.damage_data.items():
            if self.damage_vars[damage].get() == 1:
                total_damage += price
        return total_damage

    def set_total_price(self, total_price):
        self.total_price = total_price
        self.total_price_var.set(f"₱{total_price:.2f}")

    def load_data_from_db(self):
        start = self.start
        self.tree.delete(*self.tree.get_children())
        data = db_manager.Get.all_ongoing_rentals_with_preliminary(cursor=db_manager.cursor)
        for  index, rental in enumerate(data):
            if start > index:
                continue
            self.tree.insert(
                "", 
                "end", 
                values=tuple(str(value) for value in rental)
            )

    def on_plate_selected(self, event=None):
        selected_id = self.rent_id_combobox.get()
        self.tree.delete(*self.tree.get_children())

        if selected_id == "Select Rent ID":
            self.load_data_from_db()
        else:
            data = db_manager.Get.get_ongoing_rental_by_id(cursor=db_manager.cursor, rental_id=selected_id)

            if data:
                self.tree.insert(
                    "", 
                    "end", 
                    values=(
                        str(data[0]),  # rental_id
                        str(data[1]),  # plate_number
                        str(data[2]),  # rental_date
                        str(data[3]),  # return_date
                        str(data[4]),  # preliminary_total
                        str(data[5])   # status
                    )
                )
                self.set_total_price(total_price=data[4])


    def refresh(self):
        self.load_data_from_db()
        ongoing_rental_ids = db_manager.Get.all_ongoing_rental_ids(cursor=db_manager.cursor)
        self.rent_id_combobox["values"] = ["Select Rent ID"] + ongoing_rental_ids


    def calculate_date_punishment(self):
        rental_id = self.rent_id_combobox.get()
        
        rental_date = db_manager.Get.get_rental_date(cursor=db_manager.cursor, rental_id=rental_id)
        return_date = db_manager.Get.get_rental_return_date(cursor=db_manager.cursor, rental_id=rental_id)

        # Convert to datetime
        start_date = datetime.strptime(rental_date, "%d/%m/%y")
        end_date = datetime.strptime(return_date, "%d/%m/%y")

        unplanned_date_str = self.return_date_entry.get()
        try:
            unplanned_date = datetime.strptime(unplanned_date_str, "%d/%m/%y")
        except ValueError:
            return Decimal(0)

        planned_rental_period = max((end_date - start_date).days, 1)

        if planned_rental_period == 0:
            planned_rental_period = 1  # Ensure the planned period is at least 1 day

        unplanned_rental_period = (unplanned_date - start_date).days

        overdue_days = max(0, unplanned_rental_period - planned_rental_period)
        
        if unplanned_date > end_date:
            overdue_days = (unplanned_date - end_date).days

        self.overdue_days_var.set(str(overdue_days))

        penalty = Decimal(overdue_days * self.car_penalty_cost)


        self.calculate_penalty(overdue_days=overdue_days)

        return penalty
    
    def calculate_penalty(self, overdue_days):
        # the penalty formula
        user_penalty = -((overdue_days) * self.rent_overdue_multiplier)
        if user_penalty == 0:
            user_penalty += 15 

        damage_len = len(self.selected_damages) * self.rent_damage_multiplier
        user_penalty -= damage_len
        self.user_score_penalty = user_penalty


    def clear(self):
        
        self.total_price = 0
        self.selected_damages = []
        self.user_score_penalty = 0
        
    
        self.rent_id_combobox.set("Select Rent ID") 
        self.return_date_entry.delete(0, tk.END) 
        self.overdue_days_var.set("") 
        self.total_price_var.set(f"₱{self.total_price:.2f}") 
        self.load_data_from_db()

        for damage, var in self.damage_vars.items():
            var.set(0)

        self.rent_id_combobox["values"] = ["Select Rent ID"] + db_manager.Get.all_ongoing_rental_ids(cursor=db_manager.cursor)

    
    def block_scroll(self, event):
        return "break"