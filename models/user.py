from config import _DB as db
from utils.db_connection import connectToMySQL


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["nombre"]
        self.email = data["email"]
        self.password = data["contraseña"]
        self.id_user_type = data["id_tipo_de_usuario"]
        self.id_sex_interest = data["id_interes_sexo"]

    @classmethod
    def insert_user(cls, data):
        try:
            table = "usuarios"
            query = f"""insert into `{table}` (nombre, email, contraseña, id_tipo_de_usuario, id_interes_sexo)
             values ("{data['nombre']}", "{data['email']}", "{data['password']}", {data['user_type']}, {data['interest_sex']})
            """
            result = connectToMySQL(db).query_db(query)
            
            return 200 if result else 500
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    @classmethod
    def user_exists(self, email):
        try:
            table = "usuarios"
            query = f"""
            select email from {table} where email = '{email}'
            """
            result = connectToMySQL(db).query_db(query)
            return result
        except Exception as e:
            raise Exception(f"Error: {e}")
