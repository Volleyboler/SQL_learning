import psycopg2


class ClientsDB:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password
        self._conn, self._cur = self.__create_db_connect()

    def __del__(self):
        self._cur.close()
        self._conn.close()

    def __create_db_connect(self):
        self._conn = psycopg2.connect(
            host=self.__host,
            database=self.__database,
            user=self.__user,
            password=self.__password,
        )
        self._cur = self._conn.cursor()
        return self._conn, self._cur

    def create_tables(self):
        self._cur.execute("""
        CREATE TABLE IF NOT EXISTS Clients(
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
            );
        
        CREATE TABLE IF NOT EXISTS PhoneNumbers(
            id SERIAL PRIMARY KEY,
            phone_number TEXT NOT NULL,
            client_id INTEGER NOT NULL REFERENCES Clients(id)
            );
        """)
        self._conn.commit()

    def add_client(self, first_name: str, last_name: str, email: str, phones=None):
        self._cur.execute("""
        INSERT INTO Clients(first_name, last_name, email) VALUES(%s, %s, %s);
        """,
                          (first_name, last_name, email)
                          )
        client_id = self._get_client_id_by_email(email)
        self._conn.commit()
        if phones:
            for phone in phones:
                self.add_phone(client_id, phone)

    def add_phone(self, client_id: int, phone: str):
        self._cur.execute("""
        INSERT INTO PhoneNumbers(client_id, phone_number) VALUES(%s, %s);
        """,
                          (client_id, phone,)
                          )
        self._conn.commit()

    def change_client(self, client_id: int, first_name=None, last_name=None, email=None, phones=None):
        if first_name:
            self._cur.execute("""
            UPDATE Clients SET first_name=%s WHERE id=%s;
            """,
                              (first_name, client_id)
                              )
        if last_name:
            self._cur.execute("""
            UPDATE Clients SET last_name=%s WHERE id=%s;
            """,
                              (last_name, client_id)
                              )
        if email:
            self._cur.execute("""
            UPDATE Clients SET email=%s WHERE id=%s;
            """,
                              (email, client_id)
                              )
        if phones:
            self.delete_all_phones(client_id)
            for phone in phones:
                self.add_phone(client_id, phone)
        self._conn.commit()

    def delete_phone(self, client_id: int, phone: str):
        self._cur.execute("""
        DELETE FROM PhoneNumbers WHERE client_id=%s and phone_number=%s;
        """,
                          (client_id, phone,)
                          )
        self._conn.commit()

    def delete_all_phones(self, client_id: int):
        self._cur.execute("""
        DELETE FROM PhoneNumbers WHERE client_id=%s;
        """,
                          (client_id,)
                          )
        self._conn.commit()

    def delete_client(self, client_id: int):
        self._cur.execute("""
        DELETE FROM PhoneNumbers WHERE client_id=%s;
                          """,
                          (client_id,)
                          )
        self._cur.execute("""
        DELETE FROM Clients WHERE id=%s;
                          """,
                          (client_id,)
                          )
        self._conn.commit()

    def find_client(self, first_name=None, last_name=None, email=None, phone=None) -> int:
        if first_name:
            search_condition_str = "first_name=%s"
            variable_tuple = (first_name, )
        elif last_name:
            search_condition_str = "last_name=%s"
            variable_tuple = (last_name,)
        elif email:
            search_condition_str = "email=%s"
            variable_tuple = (email,)
        elif phone:
            search_condition_str = "phone_number=%s"
            variable_tuple = (phone,)
        else:
            return -1
        self._cur.execute(f"""
                SELECT C.id FROM Clients C JOIN PhoneNumbers P ON C.id=P.client_id WHERE {search_condition_str};
                          """,
                          variable_tuple)
        return self._cur.fetchone()[0]

    def _get_client_id_by_email(self, email: str) -> int:
        self._cur.execute("""
        SELECT id FROM Clients WHERE email=%s;
                          """,
                          (email,)
                          )
        return self._cur.fetchone()[0]


db = ClientsDB(host="localhost",
               database="clients_db",
               user="postgres",
               password="piroman")
db.create_tables()
db.add_client("Victor", "Petrov", "test2@mail.com", phones=["13894614891", "389136841654"])
db.add_client("Ivan", "Ivanov", "test@mail.com", phones=["456481854645", "23048210948"])
db.add_client("Ilon", "Mask", "test3@mail.com", phones=["16876941488", "46841351486"])
first_id = db.find_client(last_name="Petrov")
second_id = db.find_client(first_name="Ivan")
third_id = db.find_client(phone="46841351486")
db.delete_all_phones(first_id)
db.add_phone(second_id, "84684121654")
db.change_client(first_id, first_name="Peter", email="test5@mail.com")
db.delete_client(third_id)
db.delete_phone(second_id, "23048210948")
