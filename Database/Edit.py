

class Edit:


    @staticmethod
    def edit_user_role(cursor, conn, user_id, user_role):
        cursor.execute("USE vehicle_management")

        # Get role_id
        cursor.execute("SELECT id FROM roles WHERE name = %s", (user_role,))
        role = cursor.fetchone()
        if not role:
            return 

        role_id = role[0]

        # Update user's role
        cursor.execute("UPDATE users SET role_id = %s WHERE id = %s", (role_id, user_id))
        conn.commit()

    def edit_car_availability(cursor, conn, licensePlate, newStatus):
        cursor.execute("""
            SELECT id FROM availability_statuses
            WHERE status = %s
        """, (newStatus,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"Availability status '{newStatus}' does not exist.")

        availability_id = result[0]

        # Update the car's availability status
        cursor.execute("""
            UPDATE cars
            SET availability_id = %s
            WHERE plate_number = %s
        """, (availability_id, licensePlate))

        conn.commit()

    @staticmethod
    def mark_car_to_be_deleted(cursor, conn, license_plate):
        try:
            cursor.execute("""
                UPDATE cars
                SET deletion_status = 'To Be Deleted'
                WHERE plate_number = %s
            """, (license_plate,))
            
            conn.commit() 

        except Exception as e:
            raise Exception(f"Error marking car for deletion: {str(e)}")

    @staticmethod
    def mark_car_as_none(cursor, conn, license_plate):
        try:
            cursor.execute("""
                UPDATE cars
                SET deletion_status = 'None'
                WHERE plate_number = %s
            """, (license_plate,))
            
            conn.commit()
        
        except Exception as e:
            raise Exception(f"Error removing car for deletion: {str(e)}")
        
    @staticmethod
    def edit_car_price_by_plate(cursor, conn, license_plate, new_price):
        try:
            cursor.execute("""
                UPDATE cars
                SET daily_rental_price = %s
                WHERE plate_number = %s
            """, (new_price, license_plate))
            
            conn.commit()
        
        except Exception as e:
            raise Exception(f"Error updating price for car with plate '{license_plate}': {str(e)}")
        
    @staticmethod
    def edit_service_to_available(cursor, conn, service_name):
        try:
            cursor.execute("""
                SELECT id FROM service_statuses WHERE status_name = 'Available'
            """)
            available_status = cursor.fetchone()

            if not available_status:
                raise Exception("Status 'Available' not found in the service_statuses table.")

            available_status_id = available_status[0]

            cursor.execute("""
                UPDATE services
                SET status_id = %s
                WHERE service_name = %s
            """, (available_status_id, service_name))

            conn.commit()

        except Exception as e:
            raise Exception(f"Error updating service status to 'Available': {str(e)}")
            
    @staticmethod
    def edit_customer_reputation(conn, cursor, customer_id, reputation_to_add):
        cursor.execute("USE vehicle_management")
        
        cursor.execute("""
            UPDATE customers
            SET reputation = reputation + %s
            WHERE id = %s
        """, (reputation_to_add, customer_id))
        
        conn.commit()

        if cursor.rowcount == 0:
            raise ValueError(f"No customer found with id {customer_id}.")
        
    @staticmethod
    def edit_car_availability_to_available(conn, cursor, rent_id):
        cursor.execute("USE vehicle_management")

        cursor.execute("""
            SELECT r.car_id
            FROM rentals r
            WHERE r.id = %s
        """, (rent_id,))
        
        result = cursor.fetchone()
        
        if not result:
            raise ValueError(f"No rental found with id {rent_id}.")
        
        car_id = result[0]

        cursor.execute("""
            SELECT id
            FROM availability_statuses
            WHERE status = 'Available'
        """)
        
        available_status = cursor.fetchone()
        
        if not available_status:
            raise ValueError("No 'Available' status found in availability_statuses table.")
        
        available_status_id = available_status[0]

        cursor.execute("""
            UPDATE cars
            SET availability_id = %s
            WHERE id = %s
        """, (available_status_id, car_id))

        conn.commit()


    @staticmethod
    def edit_rental_as_returned(conn, cursor, rent_id):
        cursor.execute("USE vehicle_management")
        
        cursor.execute("""
            UPDATE rentals
            SET status = 'Returned'
            WHERE id = %s
        """, (rent_id,))
        
        conn.commit()
        
        if cursor.rowcount == 0:
            raise ValueError(f"No rental found with id {rent_id}.")
        
    
    @staticmethod
    def update_total_amount(cursor, rental_id, new_total_amount):
        query = """
            UPDATE rentals
            SET total_amount = %s
            WHERE id = %s
        """
        cursor.execute(query, (new_total_amount, rental_id))