

class Get:
    @staticmethod
    def get_role_id(conn, cursor, name):
        cursor.execute("USE vehicle_management")
        cursor.execute("SELECT id FROM roles WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    

    @staticmethod
    def get_user_data(conn, cursor, email, password):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT id, first_name, last_name, email, role_id 
            FROM users WHERE email = %s AND password = %s
        """, (email, password))
        user = cursor.fetchone()
        
        if user:
            cursor.execute("SELECT name FROM roles WHERE id = %s", (user[4],))
            role = cursor.fetchone()[0]
            return {
                "id": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "email": user[3],
                "role": role
            }
        return None
    
    @staticmethod
    def get_all_user_ids(cursor, conn):
        cursor.execute("USE vehicle_management")
        cursor.execute("SELECT id FROM users")
        return [row[0] for row in cursor.fetchall()]
    

    @staticmethod
    def get_all_users_data(cursor, conn):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT 
                users.id, 
                users.first_name, 
                users.last_name, 
                users.email, 
                roles.name AS role
            FROM users
            JOIN roles ON users.role_id = roles.id
        """)
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "role": row[4]
            } for row in rows
        ]

    @staticmethod
    def get_all_services_data(cursor):
        try:
            cursor.execute("""
                SELECT s.service_name, s.price, ss.status_name
                FROM services s
                JOIN service_statuses ss ON s.status_id = ss.id
                ORDER BY s.service_name ASC 
            """)

          
            services = cursor.fetchall()

            services_array = [
                {'service_name': service[0], 'price': service[1], 'status_name': service[2]}
                for service in services
            ]
            
            return services_array

        except Exception as e:
            raise Exception(f"Error retrieving services: {str(e)}")

    @staticmethod
    def get_all_cars_data(cursor):
        try:
            cursor.execute("""
                SELECT 
                    c.id, 
                    cp.name AS producer_name, 
                    c.model_name, 
                    c.car_year, 
                    ft.type AS fuel_type, 
                    t.type AS transmission,
                    availability_statuses.status AS availability_status,  -- This will return the availability status name
                    c.daily_rental_price, 
                    c.seats, 
                    c.plate_number, 
                    c.deletion_status
                FROM cars c
                JOIN car_producers cp ON c.producer_id = cp.id
                JOIN fuel_types ft ON c.fuel_type_id = ft.id
                JOIN transmissions t ON c.transmission_id = t.id
                JOIN availability_statuses ON c.availability_id = availability_statuses.id
                ORDER BY cp.name ASC
            """)

            cars_data = cursor.fetchall()

            return cars_data
        except Exception as e:
            raise Exception(f"Error fetching car data: {str(e)}")
        
    @staticmethod
    def get_all_pending_services(cursor):
        try:
            cursor.execute("""
                SELECT s.service_name, s.price, ss.status_name
                FROM services s
                JOIN service_statuses ss ON s.status_id = ss.id
                WHERE ss.status_name = 'Pending'
                ORDER BY s.service_name ASC
            """)

            services = cursor.fetchall()

            services_array = [
                {'service_name': service[0], 'price': service[1], 'status_name': service[2]}
                for service in services
            ]
            
            return services_array

        except Exception as e:
            raise Exception(f"Error retrieving pending services: {str(e)}")
        
    @staticmethod
    def get_all_pending_service_names(cursor):
        try:
          
            cursor.execute("""
                SELECT s.service_name
                FROM services s
                JOIN service_statuses ss ON s.status_id = ss.id
                WHERE ss.status_name = 'Pending'
            """)

            services = cursor.fetchall()

            service_names = [service[0] for service in services]
            
            return service_names

        except Exception as e:
            raise Exception(f"Error retrieving pending service names: {str(e)}")
            
    @staticmethod
    def get_all_cars_data_to_be_deleted(cursor):
        cursor.execute("""
            SELECT 
                c.id, 
                cp.name AS producer_name, 
                c.model_name, 
                c.car_year, 
                ft.type AS fuel_type, 
                t.type AS transmission,
                availability_statuses.status AS availability_status,  
                c.daily_rental_price, 
                c.seats, 
                c.plate_number, 
                c.deletion_status
            FROM cars c
            JOIN car_producers cp ON c.producer_id = cp.id
            JOIN fuel_types ft ON c.fuel_type_id = ft.id
            JOIN transmissions t ON c.transmission_id = t.id
            JOIN availability_statuses ON c.availability_id = availability_statuses.id
            WHERE c.deletion_status = 'To Be Deleted'
            ORDER BY cp.name ASC
        """)
        
        return cursor.fetchall()
    
    @staticmethod
    def get_all_cars_plate_data_to_be_deleted(cursor):
        cursor.execute("""
            SELECT c.plate_number
            FROM cars c
            WHERE c.deletion_status = 'To Be Deleted'
            ORDER BY c.plate_number ASC
        """)
        
        return cursor.fetchall()



    @staticmethod
    def get_car_data_by_license_plate(cursor, license_plate):
        cursor.execute("""
            SELECT 
                c.id, 
                cp.name AS producer_name, 
                c.model_name, 
                c.car_year, 
                ft.type AS fuel_type, 
                t.type AS transmission,
                availability_statuses.status AS availability_status,  
                c.daily_rental_price, 
                c.seats, 
                c.plate_number, 
                c.deletion_status
            FROM cars c
            JOIN car_producers cp ON c.producer_id = cp.id
            JOIN fuel_types ft ON c.fuel_type_id = ft.id
            JOIN transmissions t ON c.transmission_id = t.id
            JOIN availability_statuses ON c.availability_id = availability_statuses.id
            WHERE c.plate_number = %s
        """, (license_plate,))
        
        result = cursor.fetchone()
        
        return result
        
    @staticmethod
    def get_all_pending_cars_data(cursor):
        try:
            cursor.execute("""
                SELECT 
                    c.id, 
                    cp.name AS producer_name, 
                    c.model_name, 
                    c.car_year, 
                    ft.type AS fuel_type, 
                    t.type AS transmission,
                    availability_statuses.status AS availability_status,  
                    c.daily_rental_price, 
                    c.seats, 
                    c.plate_number, 
                    c.deletion_status
                FROM cars c
                JOIN car_producers cp ON c.producer_id = cp.id
                JOIN fuel_types ft ON c.fuel_type_id = ft.id
                JOIN transmissions t ON c.transmission_id = t.id
                JOIN availability_statuses ON c.availability_id = availability_statuses.id
                WHERE availability_statuses.status = 'Pending'
                ORDER BY c.id ASC
            """)
            
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching pending car data: {e}")
            return []

        
    @staticmethod
    def get_all_producer_names(cursor):
        try:
            cursor.execute("""
                SELECT name FROM car_producers
            """)
            
            producer_names = cursor.fetchall()
            return [producer[0] for producer in producer_names]
        
        except Exception as e:
            raise Exception(f"Error fetching producer names: {str(e)}")
        
    @staticmethod
    def get_all_transmission_types(cursor):
        try:
            cursor.execute("""
                SELECT type FROM transmissions
            """)
            
            transmission_types = cursor.fetchall()
            
            return [transmission[0] for transmission in transmission_types]
        
        except Exception as e:
            raise Exception(f"Error fetching transmission types: {str(e)}")
        
    @staticmethod
    def get_all_fuel_types(cursor):
        try:
            cursor.execute("""
                SELECT type FROM fuel_types
            """)
            
            fuel_types = cursor.fetchall()
            
            return [fuel_type[0] for fuel_type in fuel_types]
        
        except Exception as e:
            raise Exception(f"Error fetching fuel types: {str(e)}")
        
    @staticmethod
    def get_all_plate_numbers(cursor):
        cursor.execute("""
            SELECT plate_number FROM cars
        """)
        return cursor.fetchall()
    
    @staticmethod
    def get_all_pending_plate(cursor):
        cursor.execute("""
            SELECT c.plate_number
            FROM cars c
            JOIN availability_statuses a ON c.availability_id = a.id
            WHERE a.status = 'Pending'
        """)
        return cursor.fetchall()
    
    @staticmethod
    def get_all_license_plates_for_available_or_maintenance(cursor):
        try:
            cursor.execute("""
                SELECT c.plate_number
                FROM cars c
                JOIN availability_statuses AS status ON c.availability_id = status.id
                WHERE status.status IN ('Available', 'Maintenance')
            """)

            license_plates = cursor.fetchall()

            return [plate[0] for plate in license_plates]
        
        except Exception as e:
            raise Exception(f"Error fetching license plates for available or maintenance cars: {str(e)}")

    @staticmethod
    def get_all_available_license_plate(cursor):
        try:
            cursor.execute("""
                SELECT c.plate_number
                FROM cars c
                JOIN availability_statuses AS status ON c.availability_id = status.id
                WHERE status.status IN ('Available')
            """)

            license_plates = cursor.fetchall()

            return [plate[0] for plate in license_plates]
        
        except Exception as e:
            raise Exception(f"Error fetching license plates for available or maintenance cars: {str(e)}")



    @staticmethod
    def get_car_availability_by_plate(cursor, license_plate):
        try:
            cursor.execute("""
                SELECT status.status
                FROM cars c
                JOIN availability_statuses AS status ON c.availability_id = status.id
                WHERE c.plate_number = %s
            """, (license_plate,))

            availability_status = cursor.fetchone()

            if availability_status:
                return availability_status[0]
            else:
                return None

        except Exception as e:
            raise Exception(f"Error fetching availability for car with plate {license_plate}: {str(e)}")
        

    @staticmethod
    def get_all_customer_names(cursor):
        try:
            cursor.execute("""
                SELECT CONCAT(first_name, ' ', last_name) AS full_name
                FROM customers
                ORDER BY full_name ASC
            """)
            customer_names = cursor.fetchall()

            return [row[0] for row in customer_names] if customer_names else []

        except Exception as e:
            raise Exception(f"Error fetching customer names: {str(e)}")
        
    @staticmethod
    def get_all_service_names_and_prices(cursor):
        try:
            cursor.execute("""
                SELECT s.service_name, s.price
                FROM services s
                JOIN service_statuses ss ON s.status_id = ss.id
                WHERE ss.status_name = 'Available'
                ORDER BY s.service_name ASC
            """)
            services = cursor.fetchall()

            return {service_name: float(price) for service_name, price in services} if services else {}

        except Exception as e:
            raise Exception(f"Error fetching available services and prices: {str(e)}")
        
    @staticmethod
    def get_car_price_by_plate(cursor, plate_number):
        try:
            cursor.execute("""
                SELECT daily_rental_price
                FROM cars
                WHERE plate_number = %s
            """, (plate_number,))
            
            result = cursor.fetchone()
            return float(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Error fetching price for car with plate {plate_number}: {str(e)}")
        
    @staticmethod
    def get_service_price_by_name(cursor, service_name):
        try:
            cursor.execute("""
                SELECT price
                FROM services
                WHERE service_name = %s
            """, (service_name,))
            
            result = cursor.fetchone()
            return float(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Error fetching price for service '{service_name}': {str(e)}")
        
    @staticmethod
    def get_user_reputation(cursor, full_name):
        try:
            parts = full_name.rsplit(" ", 1)
            if len(parts) == 2:
                first_name, last_name = parts
            else:
                first_name, last_name = parts[0], None
            
            cursor.execute("""
                SELECT reputation 
                FROM customers 
                WHERE first_name = %s AND last_name = %s
            """, (first_name, last_name))
            
            result = cursor.fetchone()
            return int(result[0]) if result else None

        except Exception as e:
            raise Exception(f"Error fetching reputation for customer '{full_name}': {str(e)}")
        
    @staticmethod
    def get_user_reputation_by_email(cursor, email):
        cursor.execute("SELECT reputation FROM customers WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return None

        

    @staticmethod
    def get_all_customers(cursor):
        cursor.execute("""
            SELECT first_name, last_name, email, phone_number, address, license
            FROM customers
            ORDER BY first_name ASC
        """)
        rows = cursor.fetchall()

        return [
            {
                "first_name": row[0],
                "last_name": row[1],
                "email": row[2],
                "phone_number": row[3],
                "address": row[4],
                "license": row[5]
            }
            for row in rows
        ]
    
    @staticmethod
    def get_all_customer_emails(cursor):
        cursor.execute("SELECT email FROM customers")
        return [row[0] for row in cursor.fetchall()]
    
    def get_all_rentals(self, cursor):
        query = """
            SELECT 
                cars.plate_number,        
                rentals.rental_date,
                rentals.return_date,   
                rentals.total_amount,  
                rentals.status    
            FROM rentals
            JOIN cars ON rentals.car_id = cars.id
            ORDER BY rentals.rental_date DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    
    @staticmethod
    def all_ongoing_rentals_with_preliminary(cursor):
        query = """
            SELECT 
                rentals.id,
                cars.plate_number,
                rentals.rental_date,
                rentals.return_date,
                rentals.preliminary_total,
                rentals.status
            FROM rentals
            JOIN cars ON rentals.car_id = cars.id
            WHERE rentals.status = 'ongoing'
        """
        cursor.execute(query)
        return cursor.fetchall()
    
    @staticmethod
    def get_ongoing_rental_by_id(cursor, rental_id):
        query = """
            SELECT 
                rentals.id,
                cars.plate_number,
                rentals.rental_date,
                rentals.return_date,
                rentals.preliminary_total,
                rentals.status
            FROM rentals
            JOIN cars ON rentals.car_id = cars.id
            WHERE rentals.status = 'ongoing' AND rentals.id = %s
        """
        cursor.execute(query, (rental_id,))
        return cursor.fetchone()
        
        
    @staticmethod
    def all_ongoing_rental_ids(cursor):
        query = """
            SELECT 
                rentals.id
            FROM rentals
            WHERE rentals.status = 'ongoing'
        """
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    
    @staticmethod
    def get_rental_return_date(cursor, rental_id):
        query = "SELECT return_date FROM rentals WHERE id = %s"
        cursor.execute(query, (rental_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    @staticmethod
    def get_rental_date(cursor, rental_id):
        query = "SELECT rental_date FROM rentals WHERE id = %s"
        cursor.execute(query, (rental_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    @staticmethod
    def get_customer_full_name_by_rent_id(conn, cursor, rent_id):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT CONCAT(c.first_name, ' ', c.last_name) AS full_name
            FROM rentals r
            JOIN customers c ON r.customer_id = c.id
            WHERE r.id = %s
        """, (rent_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    @staticmethod
    def get_services_by_rent_id(conn, cursor, rent_id):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT s.id, s.service_name  -- Adjust column names based on your schema
            FROM rental_services rs
            JOIN services s ON rs.service_id = s.id
            WHERE rs.rental_id = %s
        """, (rent_id,))
        
        services = cursor.fetchall()
        
        service_map = {service[0]: service[1] for service in services}
        
        return service_map
    
    @staticmethod
    def get_downpayment_by_rent_id(conn, cursor, rent_id):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT downpayment_amount
            FROM rentals
            WHERE id = %s
        """, (rent_id,))
        
        result = cursor.fetchone()
        
        return result[0] if result else None
    
    @staticmethod
    def get_services_by_rent_id_with_price(conn, cursor, rent_id):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT s.service_name, s.price
            FROM rental_services rs
            JOIN services s ON rs.service_id = s.id
            WHERE rs.rental_id = %s
        """, (rent_id,))
        
        services = cursor.fetchall()

        return services
    
    @staticmethod
    def get_customer_id_by_rent_id(conn, cursor, rent_id):
        cursor.execute("USE vehicle_management")
        cursor.execute("""
            SELECT r.customer_id
            FROM rentals r
            WHERE r.id = %s
        """, (rent_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    

    @staticmethod
    def get_car_count_by_status(cursor, status):
        query = """
            SELECT COUNT(cars.id)
            FROM cars
            JOIN availability_statuses ON cars.availability_id = availability_statuses.id
            WHERE availability_statuses.status = %s
        """
        
        cursor.execute(query, (status,))
        result = cursor.fetchone()
        return result[0] if result else 0
    
    @staticmethod
    def get_service_count_by_status(cursor, status):
        query = """
            SELECT COUNT(services.id)
            FROM services
            JOIN service_statuses ON services.status_id = service_statuses.id
            WHERE service_statuses.status_name = %s
        """
        
        cursor.execute(query, (status,))
        result = cursor.fetchone()
        return result[0] if result else 0
    
    @staticmethod
    def get_car_count_by_deletion_status(cursor, deletion_status):
        query = """
            SELECT COUNT(cars.id)
            FROM cars
            WHERE cars.deletion_status = %s
        """
        
        cursor.execute(query, (deletion_status,))
        result = cursor.fetchone()
        return result[0] if result else 0
    
    @staticmethod
    def get_top_renters(cursor, limit=3):
        query = """
            SELECT c.first_name, c.last_name, COUNT(r.id) AS total_rentals
            FROM customers c
            LEFT JOIN rentals r ON c.id = r.customer_id
            GROUP BY c.id
            ORDER BY total_rentals DESC
            LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()

        # Pad the results with "None" if fewer than 3 results
        while len(results) < limit:
            results.append(("None", "None", 0))  # Pad with a tuple that has 3 values

        # Format results as tuples ("name", "X rentals")
        formatted_results = [(f"{first_name} {last_name}", f"{total_rentals} rentals") for first_name, last_name, total_rentals in results]
        
        return formatted_results
    
    def get_top_cars(cursor, limit=3):
        query = """
            SELECT c.model_name, COUNT(r.id) AS total_rentals
            FROM rentals r
            JOIN cars c ON r.car_id = c.id
            GROUP BY c.id
            ORDER BY total_rentals DESC
            LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()

        while len(results) < limit:
            results.append(("None", 0))

        formatted_results = [(f"{model_name}", f"{total_rentals} rentals") for model_name, total_rentals in results]
        
        return formatted_results
    
    @staticmethod
    def get_worst_customers(cursor, limit=3):
        query = """
            SELECT first_name, last_name, reputation
            FROM customers
            ORDER BY reputation ASC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        results = cursor.fetchall()

        while len(results) < limit:
            results.append(("None", "None", 0))

        return [(f"{first} {last}", f"Reputation: {reputation}") for first, last, reputation in results]

    @staticmethod
    def get_all_rentals(cursor):
        query = """
            SELECT 
                r.id,
                CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                cars.model_name,
                r.rental_date,
                r.return_date,
                r.downpayment_amount,
                r.total_amount,
                r.status
            FROM rentals r
            JOIN customers c ON r.customer_id = c.id
            JOIN cars ON r.car_id = cars.id
            ORDER BY r.rental_date DESC
        """
        cursor.execute(query)
        return cursor.fetchall()