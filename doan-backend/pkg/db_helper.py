import pg8000
import os
import traceback


def get_all(query, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Exception occured in get_all query: {query}")
        print(e.__str__())
        trace = traceback.format_exc()
        print(f"Trace:{trace}")

        if conn is not None:
            conn.rollback()
        return []
    finally:
        if conn is not None:
            conn.close()


def execute(query, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        record_affected = cursor.execute(query, params)
        conn.commit()
        return record_affected
    except Exception as e:
        print(f"Exception occured in get_all execute: {query}")
        print(e.__str__())
        trace = traceback.format_exc()
        print(f"Trace:{trace}")
        if conn is not None:
            conn.rollback()
        return []
    finally:
        if conn is not None:
            conn.close()


def callproc(procname, args=[]):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.callproc(procname, args)
        return cursor.fetchall()
    except Exception as e:
        print(f"Exception occured in callproc query: {procname}")
        print(e.__str__())
        trace = traceback.format_exc()
        print(f"Trace:{trace}")
        if conn is not None:
            conn.rollback()
        return []
    finally:
        if conn is not None:
            conn.close()


def get_connection():
    try:
        return pg8000.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
    except Exception as e:
        print(e.__str__())
