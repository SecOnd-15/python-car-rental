import tkinter as tk
from Session.PseudoSession import Session
from tkinter import ttk
from Database.DatabaseInstance import db_manager

class StaffManagementFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start = 0
        self.app = app
        
        self.configure(bg="#f0f0f0")

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        tk.Label(self, text="Staff Management", font=("Helvetica", 26, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        self.warningText = tk.Label(self, text="", font=("Helvetica", 10, "bold"), bg="#f0f4f8", fg="red")
        self.warningText.pack(pady=(0, 10))

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=20)

        self.user_id_label = tk.Label(form_frame, text="User Id", bg="#f0f0f0", font=("Helvetica", 12))
        self.user_id_label.grid(row=0, column=0, padx=5, sticky="w")
        self.user_id_combobox = ttk.Combobox(form_frame, values=self.FilteredGetAllUserId(), state="readonly", font=("Helvetica", 20))
        self.user_id_combobox.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        self.user_role_label = tk.Label(form_frame, text="User Role", bg="#f0f0f0", font=("Helvetica", 12))
        self.user_role_label.grid(row=2, column=0, padx=5, sticky="w")
        self.user_role_combobox = ttk.Combobox(form_frame, values=["Admin", "Staff", "Manager"], state="readonly", font=("Helvetica", 20))
        self.user_role_combobox.grid(row=3, column=0, pady=5, padx=10, sticky="w")


        self.staff_role_toggle_button = tk.Button(form_frame, text="Toggle Role", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.toggle_staff_role)
        self.staff_role_toggle_button.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

        self.staff_deletion_button = tk.Button(form_frame, text="Delete Account", font=("Helvetica", 14), bg="#00998F", fg="white", bd=0, relief="sunken", command=self.delete_account)
        self.staff_deletion_button.grid(row=6, column=0, pady=5, padx=10, sticky="ew")

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

        self.tree = ttk.Treeview(self, columns=("id", "first_name", "last_name", "email", "role"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("role", text="Role")

        self.tree.column("id", width=100)
        self.tree.column("first_name", width=150)
        self.tree.column("last_name", width=150)
        self.tree.column("email", width=200)
        self.tree.column("role", width=100)

        
        self.load_data_from_db()

        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Update ang value sa combobox once ma press para I check if naay new cars or updated cars
        self.user_id_combobox.bind("<Enter>", self.check_new_user_update_on_focus_in)

        self.tree.bind("<MouseWheel>", self.block_scroll)       
        self.tree.bind("<Button-4>", self.block_scroll)         
        self.tree.bind("<Button-5>", self.block_scroll) 

    def delete_account(self):
        user_id = self.user_id_combobox.get()
       
        try:

            if not user_id.strip():
                raise ValueError("User Id is required.")
            
            
            db_manager.Delete.delete_user(
                cursor=db_manager.cursor,
                conn=db_manager.conn,
                id=user_id
            )
            self.warningText.config(text=f"Successfully deleted user id:{user_id}", fg="green")
            self.clear()
            self.load_data_from_db()
        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")
            return


    def toggle_staff_role(self):
        user_id = self.user_id_combobox.get()
        user_role = self.user_role_combobox.get()
       
        try:

            if not user_role.strip():
                raise ValueError("User role is required.")

            if not user_id.strip():
                raise ValueError("License plate is required.")
            
           
            db_manager.Edit.edit_user_role(
                cursor=db_manager.cursor,
                conn=db_manager.conn,
                user_id=user_id,
                user_role=user_role
            )
            self.warningText.config(text="Successfully edited user role", fg="green")
            self.clear()
            self.load_data_from_db()
        except ValueError as e:
            self.warningText.config(text=str(e), fg="red")
            return


    def check_new_user_update_on_focus_in(self, event):
        self.user_id_combobox.config(values=self.FilteredGetAllUserId())

    # Para di ma apil ang current user sa change role
    def FilteredGetAllUserId(self):
        data = db_manager.Get.get_all_user_ids(
            cursor=db_manager.cursor,
            conn=db_manager.conn
        )
        filtered = [user_id for user_id in data if user_id != Session.session_id]
        return filtered


    def load_data_from_db(self):
        # FOR RELOADING
        for row in self.tree.get_children():
            self.tree.delete(row)

        #TODO: WRONG?
        data = db_manager.Get.get_all_users_data(
            cursor=db_manager.cursor,
            conn=db_manager.conn
        )

        for index, user in enumerate(data):
            if self.start > index:
                continue
            self.tree.insert("", "end", values=(
                user["id"],
                user["first_name"],
                user["last_name"],
                user["email"],
                user["role"]
            ))


    def clear(self):
        self.user_id_combobox.set('')

    def block_scroll(self, event):
        return "break"
