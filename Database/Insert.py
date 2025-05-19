from Database.Get import Get

class Insert:
    @staticmethod
    def insert_role_if_not_exists(conn, cursor, name):
        cursor.execute("USE vehicle_management")
        cursor.execute("INSERT IGNORE INTO roles (name) VALUES (%s)", (name,))
        conn.commit()

    @staticmethod
    def insert_user_if_not_exists(conn, cursor, first_name, last_name, password, email, role_name):
        role_id = Get.get_role_id(conn, cursor, role_name)
        if role_id:
            cursor.execute("USE vehicle_management")
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO users (first_name, last_name, password, email, role_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (first_name, last_name, password, email, role_id))
                conn.commit()

    @staticmethod
    def create_hardcoded_users(conn, cursor):

        roles = ['Admin', 'Manager', 'Staff']
        for role in roles:
            Insert.insert_role_if_not_exists(conn, cursor, role)

        users = [
            ("mr", "admin", "123", "admin@gmail.com", "Admin"),
            ("mr", "Manager", "123", "manager@gmail.com", "Manager"),
            ("mr", "Staff", "123", "staff@gmail.com", "Staff")
        ]
        for first_name, last_name, password, email, role_name in users:
            Insert.insert_user_if_not_exists(conn, cursor, first_name, last_name, password, email, role_name)

    @staticmethod
    def create_hardcoded_customers(conn, cursor):
        # (first_name, last_name, email, address, phone, reputation)
        customers = [
            # Regular customers with good reputation (default 50)
            ("John", "Doe", "john.doe@example.com", "123 Elm Street", "1000000001", 50, "DL1234567890"),
            ("Jane", "Smith", "jane.smith@example.com", "456 Oak Avenue", "1000000002", 52, "DL1237567891"),
            ("Alice", "Johnson", "alice.johnson@example.com", "789 Pine Road", "1000000003", 58, "DL1345678902"),
            ("Bob", "Williams", "bob.williams@example.com", "321 Maple Blvd", "1000000004", 60, "DL1456789013"),
            ("Charlie", "Brown", "charlie.brown@example.com", "101 Birch Lane", "1000000005", 50, "DL1578934124"),
            ("Emily", "Davis", "emily.davis@example.com", "202 Cedar Street", "1000000006", 65, "DL1678902345"),
            ("Olivia", "Moore", "olivia.moore@example.com", "678 Oakwood Rd", "1000000007", 53, "DL1789023456"),
            ("David", "Taylor", "david.taylor@example.com", "432 Pinewood Blvd", "1000000008", 59, "DL1890134567"),
            ("Sophia", "Anderson", "sophia.anderson@example.com", "654 Cedarwood St", "1000000009", 55, "DL1901245678"),
            ("Liam", "Thomas", "liam.thomas@example.com", "234 Birch Lane", "1000000010", 61, "DL2012356789"),
            ("Emma", "Jackson", "emma.jackson@example.com", "321 Maple Blvd", "1000000011", 62, "DL2123467890"),
            ("Noah", "Martin", "noah.martin@example.com", "789 Pine Road", "1000000012", 50, "DL2234578901"),
            ("Lucas", "Garcia", "lucas.garcia@example.com", "567 Oak Avenue", "1000000013", 60, "DL2345689012"),
            ("Mia", "Harris", "mia.harris@example.com", "202 Cedar Street", "1000000014", 55, "DL2456790123"),
            ("Ethan", "Robinson", "ethan.robinson@example.com", "987 Oakwood Rd", "1000000015", 63, "DL2567801234"),
            ("Amelia", "Martinez", "amelia.martinez@example.com", "101 Birch Lane", "1000000016", 64, "DL2678912345"),
            ("Mason", "Clark", "mason.clark@example.com", "123 Elm Street", "1000000017", 66, "DL2789023456"),
            ("Harper", "Lewis", "harper.lewis@example.com", "654 Pinewood Blvd", "1000000018", 60, "DL2890134567"),
            ("Logan", "Walker", "logan.walker@example.com", "567 Cedarwood St", "1000000019", 59, "DL2901245678"),
            ("Ava", "Young", "ava.young@example.com", "890 Birch Lane", "1000000020", 55, "DL3012356789"),
            ("Isabella", "Allen", "isabella.allen@example.com", "432 Oak Avenue", "1000000021", 50, "DL3123467890"),
            ("Amos", "Scott", "amos.scott@example.com", "321 Maple Blvd", "1000000022", 61, "DL3234578901"),
            ("Grace", "Hill", "grace.hill@example.com", "234 Cedarwood St", "1000000023", 63, "DL3345689012"),
            ("Lily", "Adams", "lily.adams@example.com", "890 Pinewood Blvd", "1000000024", 55, "DL3456790123"),
            ("Jackson", "Nelson", "jackson.nelson@example.com", "123 Oakwood Rd", "1000000025", 58, "DL3567801234"),
            ("Leo", "Baker", "leo.baker@example.com", "456 Cedarwood St", "1000000026", 57, "DL3678912345"),
            ("Chloe", "Carter", "chloe.carter@example.com", "789 Birch Lane", "1000000027", 66, "DL3789023456"),
            ("Sebastian", "Perez", "sebastian.perez@example.com", "321 Oak Avenue", "1000000028", 60, "DL3890134567"),
            ("Zoe", "Mitchell", "zoe.mitchell@example.com", "654 Maple Blvd", "1000000029", 61, "DL3901245678"),
            ("Gabriel", "Parker", "gabriel.parker@example.com", "987 Pinewood Blvd", "1000000030", 62, "DL4012356789"),
            ("Leah", "Evans", "leah.evans@example.com", "789 Cedarwood St", "1000000031", 55, "DL4123467890"),
            ("Oliver", "Collins", "oliver.collins@example.com", "234 Birch Lane", "1000000032", 59, "DL4234578901"),
            ("Eli", "Stewart", "eli.stewart@example.com", "567 Pinewood Blvd", "1000000033", 64, "DL4345689012"),
            ("Avery", "Morris", "avery.morris@example.com", "123 Oakwood Rd", "1000000034", 60, "DL4456790123"),
            ("Gabriella", "Rogers", "gabriella.rogers@example.com", "890 Maple Blvd", "1000000035", 55, "DL4567801234"),
            ("Isaiah", "Perez", "isaiah.perez@example.com", "432 Cedarwood St", "1000000036", 62, "DL4678912345"),
            ("Scarlett", "King", "scarlett.king@example.com", "234 Maple Blvd", "1000000037", 58, "DL4789023456"),
            ("Daniel", "Green", "daniel.green@example.com", "987 Birch Lane", "1000000038", 63, "DL4890134567"),
            ("Benjamin", "Bennett", "benjamin.bennett@example.com", "321 Pinewood Blvd", "1000000039", 64, "DL4901245678"),
            ("Victoria", "Ross", "victoria.ross@example.com", "654 Oak Avenue", "1000000040", 55, "DL5012356789"),
            ("Samuel", "Wood", "samuel.wood@example.com", "890 Oakwood Rd", "1000000041", 61, "DL5123467890"),
            ("Zachary", "Gonzalez", "zachary.gonzalez@example.com", "123 Pinewood Blvd", "1000000042", 60, "DL5234578901"),
            ("Lydia", "Murray", "lydia.murray@example.com", "987 Maple Blvd", "1000000043", 59, "DL5345689012"),
            ("William", "Bell", "william.bell@example.com", "234 Cedarwood St", "1000000044", 55, "DL5456790123"),
            ("Jack", "James", "jack.james@example.com", "890 Birch Lane", "1000000045", 64, "DL5567801234"),
            ("Alice", "Ford", "alice.ford@example.com", "432 Oakwood Rd", "1000000046", 50, "DL5678912345"),
            ("Matthew", "Ward", "matthew.ward@example.com", "567 Cedarwood St", "1000000047", 59, "DL5789023456"),
            ("Riley", "Patterson", "riley.patterson@example.com", "789 Oak Avenue", "1000000048", 60, "DL5890134567"),
            ("Aidan", "Gray", "aidan.gray@example.com", "234 Pinewood Blvd", "1000000049", 55, "DL5901245678"),
            ("Grace", "Diaz", "grace.diaz@example.com", "101 Birch Lane", "1000000050", 50, "DL6012356789"),

            # Customers with bad reputation (below 20)
            ("Scammy", "McFraud", "scammy.mcfraud@scamdomain.com", "123 Fraudulent Way", "1234560001", 5, "DL12345BAD01"),
            ("Liar", "VonCheat", "liar.voncheat@scamdomain.com", "456 Fraudulent Way", "1234560002", 10, "DL12345BAD02"),
            ("Shady", "Dealer", "shady.dealer@scamdomain.com", "789 Fraudulent Way", "1234560003", 7, "DL12345BAD03"),
            ("Crook", "Stealer", "crook.stealer@scamdomain.com", "101 Fraudulent Way", "1234560004", 4, "DL12345BAD04"),
            ("Fake", "Person", "fake.person@scamdomain.com", "202 Fraudulent Way", "1234560005", 9, "DL12345BAD05"),
            ("Trick", "Master", "trick.master@scamdomain.com", "303 Fraudulent Way", "1234560006", 3, "DL12345BAD06"),
            ("Fraudy", "McLie", "fraudy.mclie@scamdomain.com", "404 Fraudulent Way", "1234560007", 2, "DL12345BAD07"),
            ("Con", "Artist", "con.artist@scamdomain.com", "505 Fraudulent Way", "1234560008", 6, "DL12345BAD08"),
            ("Rip", "Offman", "rip.offman@scamdomain.com", "606 Fraudulent Way", "1234560009", 1, "DL12345BAD09"),
            ("Deceit", "Evader", "deceit.evader@scamdomain.com", "707 Fraudulent Way", "1234560010", 8, "DL12345BAD10"),
            # And so on...
        ]

        
        for idx, (first_name, last_name, email, address, phone_number, reputation, license_number) in enumerate(customers, start=1):

            cursor.execute("""
                SELECT COUNT(*) FROM customers WHERE email = %s
            """, (email,))
            customer_exists = cursor.fetchone()[0]

            if customer_exists == 0:
                cursor.execute("""
                    INSERT INTO customers (first_name, last_name, email, phone_number, address, reputation, license)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (first_name, last_name, email, phone_number, address, reputation, license_number))

        conn.commit()
             

    @staticmethod
    def add_user(conn, cursor, first_name, last_name, email, password):
        cursor.execute("USE vehicle_management")
        
        # Default role
        role_name = 'Staff'
        
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password, role_id)
            VALUES (%s, %s, %s, %s, (SELECT id FROM roles WHERE name = %s LIMIT 1))
        """, (first_name, last_name, email, password, role_name))
        
        conn.commit()


    def create_car_producers(conn, cursor):
        car_producers = [
            "Toyota", 
            "Ford", 
            "BMW", 
            "Audi", 
            "Mercedes"
        ]

        for producer in car_producers:
            cursor.execute("SELECT COUNT(*) FROM car_producers WHERE name = %s", (producer,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO car_producers (name) VALUES (%s)", (producer,))
            
        conn.commit()

    def create_car_fuel_type(conn, cursor):
        fuel_types = [
            "Petrol",
            "Diesel",
            "Electric",
            "Hybrid",
            "Gas"
        ]

        for fuel_type in fuel_types:
            cursor.execute("SELECT COUNT(*) FROM fuel_types WHERE type = %s", (fuel_type,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO fuel_types (type) VALUES (%s)", (fuel_type,))
        
        conn.commit()

    def create_transmission(conn, cursor):
        transmissions = [
            "Automatic",
            "Manual",
            "CVT",
            "Semi-Automatic"
        ]
        
        for transmission in transmissions:
            cursor.execute("SELECT COUNT(*) FROM transmissions WHERE type = %s", (transmission,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO transmissions (type) VALUES (%s)", (transmission,))
        
           
        conn.commit()

    def create_car_availability_status(conn, cursor):
        availability_statuses = [
            "Unavailable",
            "Available",
            "Pending",
            "Maintenance"
        ]
        
        for status in availability_statuses:
            cursor.execute("SELECT COUNT(*) FROM availability_statuses WHERE status = %s", (status,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("INSERT INTO availability_statuses (status) VALUES (%s)", (status,))
            

        conn.commit()


    @staticmethod
    def create_hardcoded_cars(conn, cursor):
        cars = [
            ("Toyota", "Corolla", "2020", "Petrol", "Automatic", "Available", 150, 5, "ABC123"),
            ("Toyota", "Camry", "2021", "Hybrid", "Automatic", "Available", 180, 6, "XYZ987"),
            ("Ford", "Focus", "2019", "Diesel", "Manual", "Pending", 130, 5, "DEF456"),
            ("BMW", "3 Series", "2022", "Petrol", "Automatic", "Pending", 250, 4, "LMN789"),
            ("Audi", "A4", "2021", "Diesel", "Semi-Automatic", "Available", 220, 7, "GHI321"),
            ("Mercedes", "C-Class", "2020", "Electric", "Automatic", "Available", 300, 5, "JKL654"),
            ("Toyota", "Prius", "2020", "Hybrid", "Automatic", "Available", 200, 6, "LMN001"),
            ("Ford", "Mustang", "2021", "Petrol", "Manual", "Available", 350, 4, "DEF789"),
            ("BMW", "X5", "2021", "Diesel", "Automatic", "Maintenance", 400, 5, "ABC456"),
            ("Audi", "Q5", "2020", "Hybrid", "CVT", "Available", 350, 6, "XYZ654"),
            ("Toyota", "Yaris", "2021", "Petrol", "Manual", "Pending", 120, 5, "ABC789"),
            ("Mercedes", "E-Class", "2022", "Electric", "Semi-Automatic", "Available", 500, 7, "JKL123"),
            ("Ford", "Escape", "2021", "Hybrid", "Automatic", "Available", 250, 5, "DEF321"),
            ("BMW", "5 Series", "2022", "Petrol", "Automatic", "Pending", 450, 6, "LMN456"),
            ("Audi", "A6", "2021", "Diesel", "Manual", "Pending", 300, 5, "GHI654"),
            ("Mercedes", "S-Class", "2020", "Electric", "Automatic", "Available", 600, 7, "JKL987"),
            ("Toyota", "RAV4", "2021", "Hybrid", "Automatic", "Available", 350, 5, "LMN987"),
            ("Ford", "F-150", "2020", "Diesel", "Manual", "Available", 250, 4, "DEF123"),
            ("BMW", "Z4", "2021", "Petrol", "Automatic", "Pending", 450, 5, "LMN123"),
            ("Audi", "Q7", "2020", "Hybrid", "CVT", "Available", 450, 6, "GHI987"),
            ("Mercedes", "GLC", "2021", "Diesel", "Semi-Automatic", "Available", 400, 7, "JKL654"),
            ("Toyota", "Highlander", "2020", "Petrol", "Automatic", "Available", 350, 5, "ABC654"),
            ("Ford", "Bronco", "2021", "Diesel", "Manual", "Pending", 330, 6, "DEF654"),
            ("BMW", "M3", "2022", "Petrol", "Automatic", "Available", 500, 5, "LMN654"),
            ("Audi", "TT", "2020", "Petrol", "CVT", "Maintenance", 400, 4, "XYZ321"),
            ("Mercedes", "G-Wagon", "2021", "Diesel", "Semi-Automatic", "Available", 700, 6, "JKL321"),
            ("Toyota", "Land Cruiser", "2020", "Diesel", "Automatic", "Pending", 600, 7, "ABC987"),
            ("Ford", "Ranger", "2021", "Petrol", "Manual", "Available", 350, 5, "DEF321"),
            ("BMW", "i8", "2022", "Electric", "Automatic", "Pending", 600, 4, "LMN432"),
            ("Audi", "A3", "2021", "Diesel", "Semi-Automatic", "Available", 280, 5, "GHI432"),
            ("Mercedes", "CLA", "2020", "Petrol", "CVT", "Available", 400, 5, "JKL876"),
            ("Toyota", "Avalon", "2021", "Hybrid", "Automatic", "Available", 220, 5, "LMN654"),
            ("Ford", "Expedition", "2020", "Diesel", "Automatic", "Pending", 350, 7, "DEF876"),
            ("BMW", "X6", "2021", "Petrol", "Manual", "Available", 500, 6, "LMN987"),
            ("Audi", "S4", "2021", "Diesel", "Automatic", "Available", 350, 5, "XYZ123"),
            ("Mercedes", "AMG GT", "2022", "Petrol", "Semi-Automatic", "Pending", 700, 2, "JKL432"),
            ("Toyota", "Sienna", "2021", "Hybrid", "Automatic", "Available", 350, 7, "ABC432"),
            ("Ford", "Explorer", "2020", "Diesel", "Automatic", "Available", 300, 6, "DEF123"),
            ("BMW", "7 Series", "2021", "Petrol", "Automatic", "Pending", 550, 5, "LMN345"),
            ("Audi", "Q3", "2020", "Hybrid", "CVT", "Available", 380, 5, "GHI876"),
            ("Mercedes", "B-Class", "2021", "Electric", "Automatic", "Available", 350, 5, "JKL098"),
            ("Toyota", "Tacoma", "2020", "Diesel", "Manual", "Pending", 250, 5, "ABC654"),
            ("Ford", "Edge", "2021", "Hybrid", "Automatic", "Available", 300, 6, "DEF987"),
            ("BMW", "X4", "2021", "Petrol", "Manual", "Available", 450, 5, "LMN654"),
            ("Audi", "RS7", "2020", "Diesel", "Semi-Automatic", "Maintenance", 600, 4, "GHI543"),
            ("Mercedes", "GLS", "2021", "Hybrid", "Automatic", "Available", 700, 7, "JKL321"),
            ("Toyota", "Tundra", "2021", "Petrol", "Automatic", "Available", 350, 5, "LMN098"),
            ("Ford", "Mustang Mach-E", "2021", "Electric", "Automatic", "Available", 450, 5, "DEF678"),
            ("BMW", "8 Series", "2022", "Petrol", "Automatic", "Pending", 600, 5, "LMN876"),
            ("Audi", "Q8", "2020", "Diesel", "CVT", "Available", 500, 7, "GHI432"),
            ("Mercedes", "GLA", "2021", "Electric", "Semi-Automatic", "Available", 450, 5, "JKL876"),
            ("Toyota", "Sequoia", "2020", "Petrol", "Manual", "Pending", 400, 7, "ABC987"),
            ("Ford", "F-250", "2021", "Diesel", "Automatic", "Pending", 450, 5, "DEF543"),
            ("BMW", "X7", "2021", "Hybrid", "Automatic", "Available", 650, 7, "LMN987"),
            ("Audi", "A5", "2020", "Petrol", "Semi-Automatic", "Available", 350, 5, "GHI321"),
            ("Mercedes", "V-Class", "2021", "Diesel", "CVT", "Available", 500, 6, "JKL654"),
            ("Toyota", "Matrix", "2020", "Hybrid", "Automatic", "Available", 220, 5, "LMN123"),
            ("Ford", "Fiesta", "2020", "Petrol", "Manual", "Available", 180, 5, "DEF321"),
            ("BMW", "X3", "2021", "Diesel", "Automatic", "Pending", 400, 5, "LMN654"),
            ("Audi", "S5", "2020", "Hybrid", "CVT", "Available", 500, 5, "GHI987"),
            ("Mercedes", "G-Class", "2021", "Petrol", "Manual", "Available", 700, 5, "JKL321"),
            ("Toyota", "Land Cruiser Prado", "2021", "Diesel", "Automatic", "Available", 500, 6, "ABC876"),
            ("Ford", "Maverick", "2021", "Petrol", "Automatic", "Pending", 300, 5, "DEF987"),
            ("BMW", "X2", "2021", "Hybrid", "Semi-Automatic", "Available", 450, 4, "LMN123"),
            ("Audi", "E-Tron", "2021", "Electric", "Automatic", "Available", 550, 5, "GHI321"),
            ("Mercedes", "EQC", "2021", "Electric", "CVT", "Available", 600, 5, "JKL432"),
            ("Toyota", "Hilux", "2020", "Diesel", "Automatic", "Available", 400, 5, "ABC543"),
            ("Ford", "Puma", "2021", "Petrol", "Manual", "Available", 200, 5, "DEF543"),
            ("BMW", "3 Series Touring", "2021", "Diesel", "CVT", "Available", 400, 5, "LMN321"),
            ("Audi", "Q4", "2021", "Electric", "Semi-Automatic", "Available", 450, 5, "GHI654"),
            ("Mercedes", "Benz", "2021", "Hybrid", "Automatic", "Available", 350, 5, "JKL765"),
            ("Toyota", "Fortuner", "2021", "Petrol", "Manual", "Pending", 350, 7, "LMN432"),
            ("Ford", "Taurus", "2021", "Diesel", "Automatic", "Available", 300, 5, "DEF876"),
            ("BMW", "i4", "2022", "Electric", "Automatic", "Pending", 500, 5, "LMN234"),
            ("Audi", "A8", "2020", "Diesel", "Manual", "Available", 350, 5, "GHI432"),
            ("Mercedes", "GLA", "2021", "Hybrid", "Automatic", "Available", 450, 5, "JKL432"),
            ("Toyota", "Venza", "2020", "Hybrid", "Automatic", "Available", 230, 5, "ABC876"),
            ("Ford", "Fusion", "2021", "Petrol", "Manual", "Available", 230, 5, "DEF765"),
            ("BMW", "M4", "2022", "Petrol", "Automatic", "Available", 600, 4, "LMN654")
        ]

        for producer, model_name, car_year, fuel_type, transmission, availability_status, daily_rental_price, seats, plate_number in cars:
            cursor.execute("""
                SELECT 1 FROM cars WHERE plate_number = %s
            """, (plate_number,))
            existing_car = cursor.fetchone()
            
            if existing_car:
                continue
            
            
            cursor.execute("""
                SELECT id FROM car_producers WHERE name = %s
            """, (producer,))
            producer_id = cursor.fetchone()
            if producer_id:
                producer_id = producer_id[0]
          
            
            cursor.execute("""
                SELECT id FROM fuel_types WHERE type = %s
            """, (fuel_type,))
            fuel_type_id = cursor.fetchone()
            if fuel_type_id:
                fuel_type_id = fuel_type_id[0]
           

            cursor.execute("""
                SELECT id FROM transmissions WHERE type = %s
            """, (transmission,))
            transmission_id = cursor.fetchone()
            if transmission_id:
                transmission_id = transmission_id[0]
           
            cursor.execute("""
                SELECT id FROM availability_statuses WHERE status = %s
            """, (availability_status,))
            availability_id = cursor.fetchone()
            if availability_id:
                availability_id = availability_id[0]
           
            
            cursor.execute("""
                INSERT INTO cars (producer_id, model_name, car_year, fuel_type_id, transmission_id, availability_id, daily_rental_price, seats, plate_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (producer_id, model_name, car_year, fuel_type_id, transmission_id, availability_id, daily_rental_price, seats, plate_number))
           

        conn.commit()


    @staticmethod
    def create_hardcoded_services_statuses(cursor, conn):
        try:
            statuses = ['Pending', 'Available']

            for status in statuses:
                cursor.execute("""
                    SELECT 1 FROM service_statuses WHERE status_name = %s
                """, (status,))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute("""
                        INSERT INTO service_statuses (status_name)
                        VALUES (%s)
                    """, (status,))
            
            conn.commit()

        except Exception as e:
            raise Exception(f"Error ensuring service statuses: {str(e)}")
        
    @staticmethod
    def create_hardcoded_services(cursor, conn):
        try:
            services = [
                ('GPS Navigation', 5.00, 'Pending'),
                ('Child Seat', 7.50, 'Pending'),
                ('Additional Insurance', 15.00, 'Available'),
                ('Roadside Assistance', 10.00, 'Available'),
                ('Wi-Fi Hotspot', 8.00, 'Available'),
                ('Extended Mileage', 12.00, 'Available'),
                ('Extra Driver', 10.00, 'Available'),
                ('Toll Pass', 5.00, 'Available'),
                ('Fuel Service', 15.00, 'Available'),
                ('Snow Chains', 6.00, 'Available'),
                ('Tire Protection', 7.00, 'Available'),
                ('Bluetooth Connectivity', 4.00, 'Pending'),
                ('Luxury Car Upgrade', 50.00, 'Available'),
                ('Convertible Car Upgrade', 40.00, 'Available'),
                ('Baby Seat', 5.00, 'Pending'),
                ('Navigation App Subscription', 3.00, 'Available'),
                ('Additional Driver Insurance', 8.00, 'Available'),
                ('Off-Road Equipment Package', 20.00, 'Available'),
                ('Full Tank Option', 30.00, 'Available'),
                ('Road Trip Kit', 12.00, 'Available')
            ]

            for name, price, status_name in services:
                # Check if the status exists
                cursor.execute("""
                    SELECT id FROM service_statuses WHERE status_name = %s
                """, (status_name,))
                status = cursor.fetchone()

                if not status:
                    raise Exception(f"Status '{status_name}' not found. Run ensure_service_statuses first.")

                status_id = status[0]

                # Check if the service already exists
                cursor.execute("""
                    SELECT 1 FROM services WHERE service_name = %s
                """, (name,))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute("""
                        INSERT INTO services (service_name, price, status_id)
                        VALUES (%s, %s, %s)
                    """, (name, price, status_id))

            conn.commit()

        except Exception as e:
            raise Exception(f"Error creating hardcoded services: {str(e)}")

    @staticmethod
    def insert_car(cursor, conn, car_make, model_name, car_year, fuel_type, transmission, daily_rental_price, seats, plate_number):

        availability_status = "Pending"

        try:
            cursor.execute("SELECT id FROM car_producers WHERE name = %s", (car_make,))
            producer_id = cursor.fetchone()

            if not producer_id:
                raise ValueError(f"Producer '{car_make}' not found in the database.")

            producer_id = producer_id[0]

            cursor.execute("SELECT id FROM fuel_types WHERE type = %s", (fuel_type,))
            fuel_type_id = cursor.fetchone()

            if not fuel_type_id:
                raise ValueError(f"Fuel type '{fuel_type}' not found in the database.")

            fuel_type_id = fuel_type_id[0]

            cursor.execute("SELECT id FROM transmissions WHERE type = %s", (transmission,))
            transmission_id = cursor.fetchone()

            if not transmission_id:
                raise ValueError(f"Transmission type '{transmission}' not found in the database.")

            transmission_id = transmission_id[0] 

            cursor.execute("""
                INSERT INTO cars (producer_id, model_name, car_year, fuel_type_id, transmission_id, daily_rental_price, seats, plate_number, availability_id)
                SELECT %s, %s, %s, %s, %s, %s, %s, %s, id
                FROM availability_statuses
                WHERE status = %s
            """, (producer_id, model_name, car_year, fuel_type_id, transmission_id, daily_rental_price, seats, plate_number, availability_status))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error inserting car: {str(e)}")
        

    @staticmethod
    def insert_service(cursor, conn, service_name, price):
        try:
            cursor.execute("""
                INSERT INTO services (service_name, price, status_id)
                SELECT %s, %s, id FROM service_statuses WHERE status_name = "Pending"
            """, (service_name, price))

            conn.commit()

        except Exception as e:
            raise Exception(f"Error inserting service: {str(e)}")
        
    @staticmethod
    def add_rental(conn, cursor, customer_email, plate_number, rental_date, return_date,
                total_amount, downpayment_amount, selected_services):
        cursor.execute("USE vehicle_management")

        # Get customer ID from email
        cursor.execute("SELECT id FROM customers WHERE email = %s", (customer_email,))
        customer_row = cursor.fetchone()
        if not customer_row:
            raise ValueError("Customer not found.")
        customer_id = customer_row[0]

        # Get car ID from plate number
        cursor.execute("SELECT id FROM cars WHERE plate_number = %s", (plate_number,))
        car_row = cursor.fetchone()
        if not car_row:
            raise ValueError("Car not found.")
        car_id = car_row[0]

        # Insert rental
        cursor.execute("""
            INSERT INTO rentals (customer_id, car_id, rental_date, return_date, total_amount, preliminary_total, downpayment_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (customer_id, car_id, rental_date, return_date, total_amount, total_amount, downpayment_amount))
        rental_id = cursor.lastrowid

        # Link services to rental
        for service_name in selected_services:
            cursor.execute("SELECT id FROM services WHERE service_name = %s", (service_name,))
            service_row = cursor.fetchone()
            if service_row:
                service_id = service_row[0]
                cursor.execute("""
                    INSERT INTO rental_services (rental_id, service_id)
                    VALUES (%s, %s)
                """, (rental_id, service_id))

        conn.commit()

    @staticmethod
    def add_customer(conn, cursor, first_name, last_name, email, phone_number, address, license):
        cursor.execute("USE vehicle_management")

        cursor.execute("""
            INSERT INTO customers (first_name, last_name, email, phone_number, address, license)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone_number, address, license))

        conn.commit()