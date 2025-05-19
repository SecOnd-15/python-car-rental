

class Delete():


    @staticmethod
    def delete_user(cursor, conn, id):
        cursor.execute("USE vehicle_management")
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()


    @staticmethod
    def delete_car_by_license_plate(cursor, conn, license_plate):
        try:
            cursor.execute("""
                DELETE FROM cars
                WHERE plate_number = %s
            """, (license_plate,))
            
            if conn:
                conn.commit()
            else:
                raise Exception("No active database connection.")
        
        except Exception as e:
            print(f"Error deleting car with license plate {license_plate}: {e}")
            raise e