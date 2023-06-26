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
            query = f"""insert into `{table}` (nombre, email, contraseñaa, id_tipo_de_usuario, id_interes_sexo)
             values ("{data['nombre']}", "{data['email']}", "{data['password']}", {data['user_type']}, {data['interest_sex']})
            """
            result = connectToMySQL(db).query_db(query)
            if result:
                return 200
            else:
                return "Ocurrio un error, intente registrarse nuevamete"
        except Exception as e:
            raise Exception(f"Error: {e}")
