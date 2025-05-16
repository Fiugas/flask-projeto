import os
from re import I

import psycopg2

# Conexão à BD
def get_connection():
    return psycopg2.connect(host="aid.estgoh.ipc.pt", database="db2021155919", user="a2021155919", password="a2021155919")

# Verifica se o utilizador existe
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

# Login
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

# Insere reserva
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

# Verifica disponibilidade
def get_disponibilidade(id_quarto, data):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("EXECUTE PROCEDURE quarto_disponivel(%s, %s)", [id_quarto, data])
                disponivel = cur.fetchone()
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(conn):
            cur.close()
            conn.close()
        return disponivel

# X - Incompleto 
def pagamento():
    return "X"

# X - Incompleto 
def cancel():
    return "X"

# X - Incompleto 
def upload():
    return "X"

# X - Incompleto 
def ver_imagem():
    return "X"