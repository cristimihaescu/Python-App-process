from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_mentors(cursor):
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_applicants(cursor):
    query = """
        SELECT first_name, last_name, phone_number, email, application_code
        FROM applicant
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_last_name(cursor: RealDictCursor, last_name: str) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        WHERE last_name = %(lname)s"""
    cursor.execute(query, {'lname': last_name})
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_city_name(cursor: RealDictCursor, city: str) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        WHERE city = %(city)s"""
    cursor.execute(query, {'city': city})
    return cursor.fetchall()


@database_common.connection_handler
def get_applicants_byFirstName(cursor: RealDictCursor, applicant_name: str) -> list:
    query = """
        select first_name || ' ' || last_name as name, phone_number
        from applicant
        where lower(first_name) = lower(%(applicant_name)s);"""
    cursor.execute(query, {'applicant_name': applicant_name})
    return cursor.fetchall()


@database_common.connection_handler
def get_applicants_byEmail(cursor: RealDictCursor, email) -> list:
    email = f"%{email}%"
    query = """
        SELECT first_name || ' ' || last_name as name, phone_number
        FROM applicant
        WHERE email LIKE (%(email)s);"""
    cursor.execute(query, {'email': email})
    return cursor.fetchall()


@database_common.connection_handler
def get_byApplication_code(cursor: RealDictCursor, application_code):
    query = """
        select * from applicant
    where application_code =(%(application_code)s);  """
    cursor.execute(query, {'application_code': application_code})
    return cursor.fetchall()


@database_common.connection_handler
def update_applicant_byApplication_code(cursor: RealDictCursor, phone_number, application_code):
    cursor.execute("""UPDATE applicant SET phone_number = %s  WHERE application_code = %s""",
                   (phone_number, application_code))


@database_common.connection_handler
def adding_new_applicant(cursor, first_name, last_name, phone_number, email, application_code) -> list:
    query = f"""
            INSERT INTO applicant (first_name, last_name, phone_number, email, application_code)
            VALUES('{first_name}', '{last_name}', '{phone_number}', '{email}', '{application_code}');
            """
    cursor.execute(query)


@database_common.connection_handler
def delete_applicant(cursor, application_code: str):
    query = """DELETE
 FROM applicant where application_code = (%(application_code)s); """
    cursor.execute(query,{'application_code': application_code})