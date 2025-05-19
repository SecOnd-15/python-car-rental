import tkinter as tk
from tkinter import ttk
from Database.DatabaseManager import DatabaseManager
from Database.DatabaseInstance import db_manager

class CarDeletionApprovalFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app

        self.configure(bg="#f0f0f0")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Delete Car", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)

        self.plate_number_label = tk.Label(form_frame, text="Select Car Plate Number", bg="#f0f0f0", font=("Helvetica", 12))
        self.plate_number_label.grid(row=0, column=0, padx=5, sticky="w")

        self.plate_number_combobox = ttk.Combobox(form_frame, state="readonly", font=("Helvetica", 20))
        self.plate_number_combobox.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        self.delete_car_button = tk.Button(form_frame, text="Mark for Deletion", font=("Helvetica", 14), bg="#c0392b", fg="white", bd=0, relief="sunken", command=self.delete_car)
        self.delete_car_button.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

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

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.plate_number_combobox.bind("<Enter>", self.refresh_plate_list)
        self.plate_number_combobox.bind("<<ComboboxSelected>>", self.show_selected_plate_data)
        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 
        self.load_data_from_db()

    def delete_car(self):
        plate_number = self.plate_number_combobox.get()
        try:
            if plate_number == "Select Plate Number" or not plate_number.strip():
                raise ValueError("License plate is required.")
           
            db_manager.Delete.delete_car_by_license_plate(cursor=db_manager.cursor, conn=db_manager.conn, license_plate=plate_number)
            self.warningText.config(text="Successfully deleted car.", fg="green")
            self.clear()
            self.load_data_from_db()
        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")

    def refresh_plate_list(self, event):
        plates = db_manager.Get.get_all_cars_plate_data_to_be_deleted(cursor=db_manager.cursor)
        self.plate_number_combobox["values"] = ["Select Plate Number"] + plates
        if not self.plate_number_combobox.get():
            self.plate_number_combobox.set("Select Plate Number")

    def show_selected_plate_data(self, event):
        selected_plate = self.plate_number_combobox.get()
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

    

    def clear(self):
        self.plate_number_combobox.set("Select Plate Number")

    def block_scroll(self, event):
        return "break"
