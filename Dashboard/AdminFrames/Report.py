import tkinter as tk
from tkinter import ttk
from Database.DatabaseInstance import db_manager  # Can be kept or removed for now

class ReportFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        self.configure(bg="#f4f7fc")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Configure internal grid: 2 rows, 3 columns
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)
        self.grid_rowconfigure(1, weight=2)  # Treeview row

        # Title
        tk.Label(self, text="Car Rental Report", font=("Segoe UI", 26, "bold"),
                 bg="#f4f7fc", fg="#333").grid(row=0, column=0, columnspan=3, pady=20)

        # --- [1st Row] - Summary Boxes ---

        # [0,0] Top Users
        self.top_users_frame = tk.Frame(self, bg="#e0ecff", bd=1, relief="solid")
        self.top_users_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tk.Label(self.top_users_frame, text="Top Users", font=("Segoe UI", 14, "bold"), bg="#e0ecff").pack(pady=10)
        for name, count in db_manager.Get.get_top_renters(cursor=db_manager.cursor, limit=3):
            tk.Label(self.top_users_frame, text=f"{name} - {count}", bg="#e0ecff", font=("Segoe UI", 12)).pack(anchor="w", padx=10)

        # [0,1] Top Cars
        self.top_cars_frame = tk.Frame(self, bg="#fff4cc", bd=1, relief="solid")
        self.top_cars_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        tk.Label(self.top_cars_frame, text="Top Cars", font=("Segoe UI", 14, "bold"), bg="#fff4cc").pack(pady=10)
        for car, count in db_manager.Get.get_top_cars(cursor=db_manager.cursor, limit=3):
            tk.Label(self.top_cars_frame, text=f"{car} - {count}", bg="#fff4cc", font=("Segoe UI", 12)).pack(anchor="w", padx=10)

        # [0,2] Projected Income
        self.worst_customers_frame = tk.Frame(self, bg="#ffd6d6", bd=1, relief="solid")
        self.worst_customers_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        tk.Label(self.worst_customers_frame, text="Worst Customers", font=("Segoe UI", 14, "bold"), bg="#ffd6d6").pack(pady=10)
        for name, count in db_manager.Get.get_worst_customers(cursor=db_manager.cursor, limit=3):
            tk.Label(self.worst_customers_frame, text=f"{name} - {count}", bg="#ffd6d6", font=("Segoe UI", 12)).pack(anchor="w", padx=10)

        # --- [2nd Row] - TreeView ---
        self.tree_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        self.tree_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "User", "Car", "Rental Date", "Return Date", "Downpayment",
                    "Total", "status"),
            show="headings"
        )

        columns = {
            "ID": 40,
            "User": 150,
            "Car": 120,
            "Rental Date": 100,
            "Return Date": 100,
            "Downpayment": 120,
            "Total": 100,
            "status": 90
        }

        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center", stretch=True)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        rentals = db_manager.Get.get_all_rentals(cursor=db_manager.cursor)
        for rental in rentals:
            self.tree.insert("", "end", values=rental)


    def refresh(self):
        for widget in self.top_users_frame.winfo_children():
            if widget.cget("text") != "Top Users":
                widget.destroy()

        if not any(widget.cget("text") == "Top Users" for widget in self.top_users_frame.winfo_children()):
            tk.Label(self.top_users_frame, text="Top Users", font=("Segoe UI", 14, "bold"), bg="#e0ecff").pack(pady=10)

        for name, count in db_manager.Get.get_top_renters(cursor=db_manager.cursor, limit=3):
            tk.Label(self.top_users_frame, text=f"{name} - {count}", bg="#e0ecff", font=("Segoe UI", 12)).pack(anchor="w", padx=10)

        for widget in self.top_cars_frame.winfo_children():
            widget.destroy()

        if not any(widget.cget("text") == "Top Cars" for widget in self.top_cars_frame.winfo_children()):
            tk.Label(self.top_cars_frame, text="Top Cars", font=("Segoe UI", 14, "bold"), bg="#fff4cc").pack(pady=10)

        top_cars = db_manager.Get.get_top_cars(cursor=db_manager.cursor, limit=3)
        for car, count in top_cars:
            tk.Label(self.top_cars_frame, text=f"{car} - {count}", bg="#fff4cc", font=("Segoe UI", 12)).pack(anchor="w", padx=10)


        for row in self.tree.get_children():
            self.tree.delete(row)

        rentals = db_manager.Get.get_all_rentals(cursor=db_manager.cursor)
        for rental in rentals:
            self.tree.insert("", "end", values=rental)