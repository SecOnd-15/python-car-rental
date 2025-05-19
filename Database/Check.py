

class Check:

    @staticmethod
    def check_user_if_exist(conn, cursor, email):
        cursor.execute("USE vehicle_management")
        
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        return True if user else False
    
    @staticmethod
    def check_customer_if_exist(conn, cursor, email):
        cursor.execute("USE vehicle_management")
    
        cursor.execute("SELECT id FROM customers WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        return True if user else False
        

    @staticmethod
    def check_of_credentials_match(conn, cursor, email, password):
        cursor.execute("USE vehicle_management")
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        return user and user[1] == password
    
    @staticmethod
    def is_plate_marked_for_deletion(cursor, license_plate):
        cursor.execute("""
            SELECT deletion_status
            FROM cars
            WHERE plate_number = %s
        """, (license_plate,))
        result = cursor.fetchone()
        return result[0] == "To Be Deleted" if result else False
        

    @staticmethod
    def check_service_exists(cursor, service_name):
        try:
            cursor.execute("""
                SELECT 1 FROM services
                WHERE service_name = %s
                LIMIT 1
            """, (service_name,))
            return cursor.fetchone() is not None
        except Exception as e:
            raise Exception(f"Error checking if service exists: {str(e)}")
    