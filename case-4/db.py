from typing import List

import psycopg2


class DataBase:
    def __init__(self, database: str, login: str, password: str):
        self.__conn = None
        self.__cursor = None

        self.__database: str = database
        self.__login: str = login
        self.__password: str = password

    def __connect(self):
        self.__conn = psycopg2.connect(database=self.__database, user=self.__login, password=self.__password)

        self.__cursor = self.__conn.cursor()

    def __commit(self):
        self.__conn.commit()

    def __disconnect(self):
        self.__cursor.close()

        self.__conn.close()

    def create_db(self):
        self.__connect()

        self.__cursor.execute("""
            CREATE TABLE client (
                id serial primary key unique,
                f_name varchar(20) not null,
                s_name varchar(20) not null,
                email varchar(20) not null
            );
        """)

        self.__cursor.execute("""
            CREATE TABLE client_phones (
                id serial primary key unique,
                client_id int not null REFERENCES client(id),
                phone varchar(20) not null
            );
        """)

        self.__commit()

        self.__disconnect()

    def create_client(self, f_name: str, s_name: str, email: str, phones: List[str] = None):
        self.__connect()

        self.__cursor.execute(f"INSERT INTO client(f_name, s_name, email) VALUES(%s, %s, %s) RETURNING id",
                              (f_name, s_name, email))

        id_client: tuple = self.__cursor.fetchone()

        self.__conn.commit()

        if phones is not None:
            for phone in phones:
                self.__cursor.execute(f"INSERT INTO client_phones(client_id, phone) VALUES(%s, %s)",
                                      (int(id_client[0]), phone))

        self.__commit()

        self.__disconnect()

        return int(id_client[0])

    def add_phone(self, client_id: int, phones: List[str]):
        self.__connect()

        if phones is not None:
            for phone in phones:
                self.__cursor.execute(f"INSERT INTO client_phones(client_id, phone) VALUES(%s, %s)",
                                      (client_id, phone))

        self.__commit()

        self.__disconnect()

    def change_client(self, client_id: int, f_name: str = None, s_name: str = None, email: str = None,
                      phones: List[str] = None):
        if f_name is None and s_name is None and email is None and phones is None:
            return 'NO DATA!'
        else:
            self.__connect()

            columns = '('
            format_param = '('
            param = ()

            if f_name is not None and (s_name is not None or email is not None):
                columns += 'f_name, '
                format_param += '%s, '
                param = (f_name, client_id)
            elif f_name is not None and (s_name is None and email is None):
                columns += 'f_name'
                format_param += '%s, '
                param = (f_name, client_id)

            if s_name is not None and email is not None:
                columns += 's_name, '
                format_param += '%s, '
                param = (f_name, s_name, email, client_id)
            elif s_name is not None and email is None:
                columns += 's_name'
                format_param += '%s'
                param = (f_name, s_name, client_id)

            if email is not None:
                columns += 'email)'
                format_param += '%s)'
                if s_name is None:
                    param = (f_name, email, client_id)
                else:
                    param = (f_name, s_name, email, client_id)
            else:
                columns += ')'
                format_param += ')'

            sql = f"UPDATE client SET {columns} = {format_param} WHERE id = %s"

            self.__cursor.execute(sql, param)

            self.__commit()

            if phones is not None:
                self.__cursor.execute(f"DELETE FROM client_phones WHERE client_id = %s", [client_id])

                self.__commit()

                for phone in phones:
                    self.__cursor.execute(f"INSERT INTO client_phones(client_id, phone) VALUES(%s, %s)",
                                          (client_id, phone))

                self.__commit()

            self.__disconnect()

    def delete_phone(self, client_id, phones: List[str]):
        self.__connect()

        for phone in phones:
            self.__cursor.execute(f"DELETE FROM client_phones WHERE client_id = %s AND phone = %s", (client_id, phone))

        self.__commit()

        self.__disconnect()

    def delete_client(self, client_id):
        self.__connect()

        self.__cursor.execute(f"DELETE FROM client_phones WHERE client_id = %s", [client_id])
        self.__cursor.execute(f"DELETE FROM client WHERE id = %s", [client_id])

        self.__commit()

        self.__disconnect()

    def search_client(self, f_name: str = None, s_name: str = None, email: str = None, phone: str = None):
        if f_name is None and s_name is None and email is None and phone is None:
            return 'NO DATA!'
        else:
            self.__connect()

            sql = f"""
            SELECT c.f_name, c.s_name, c.email, STRING_AGG(cp.phone, ',') as phones
            FROM client as c INNER JOIN client_phones cp on c.id = cp.client_id
            """

            preview = False

            if f_name is not None:
                sql += f"WHERE c.f_name = '{f_name}'"
                preview = True

            if s_name is not None and not preview:
                sql += f"WHERE c.s_name = '{s_name}'"
                preview = True
            elif s_name is not None and preview:
                sql += f" and c.s_name = '{s_name}'"
                preview = True

            if email is not None and not preview:
                sql += f"WHERE c.email = '{email}'"
                preview = True
            elif email is not None and preview:
                sql += f" and c.email = '{email}'"
                preview = True

            if phone is not None and not preview:
                sql += f"WHERE cp.phone = '{phone}'"
            elif phone is not None and preview:
                sql += f" and cp.phone = '{phone}'"

            sql += '\nGROUP BY c.f_name, c.s_name, c.email;'

            self.__cursor.execute(sql)

            result = self.__cursor.fetchall()

            self.__disconnect()

            return result
