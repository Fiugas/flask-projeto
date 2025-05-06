import os
from re import I

import psycopg2


def get_connection():
    return psycopg2.connect(host="aid.estgoh.ipc.pt", database="db2021155919", user="a2021155919", password="a2021155919")
    #return psycopg2.connect(host=os.environ.get("DATABASE_HOST"), database = os.environ.get("DATABASE_NAME"), user=os.environ.get("DATABASE_USER"), password = os.environ.get("PASSWORD"))

def user_exists(user):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM users WHERE username = %s", [user["username"]])
                count = cur.fetchone()[0]
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(conn):
            cur.close()
            conn.close()
    return count > 0


def login(username, password):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password)", [username, password])
                user_tuple = cur.fetchone()
                user = None
                if user_tuple is None:
                    return None
                user = {
                    "id": user_tuple[0],
                    "username": user_tuple[1],
                }
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(conn):
            cur.close()
            conn.close()
        return user
    
def get_quartos():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM quartos")
                matchs = []
                for match_tuple in cur.fetchall():
                    match = {
                        "id_quarto": match_tuple[0],
                        "id_user": match_tuple[1],
                        "tipo_t": match_tuple[2],
                        "disponibilidade": match_tuple[3]
                    }
                    matchs.append(match)
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(conn):
            cur.close()
            conn.close()
        return matchs
    
def insert_reserva():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("EXECUTE PROCEDURE insert_reserva_fatura")
                matchs = []
                for match_tuple in cur.fetchall():
                    match = {
                        "p_id_quarto": match_tuple[0],
                        "p_check_in": match_tuple[1],
                        "p_check_out": match_tuple[2],
                        "p_valor": match_tuple[3]
                    }
                    matchs.append(match)
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(conn):
            cur.close()
            conn.close()
        return matchs