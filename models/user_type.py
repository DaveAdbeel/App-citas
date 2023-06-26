from config import _DB as db
from utils.db_connection import connectToMySQL


class User_Type:
    def __init__(self, data):
        self.id = data["id"]
        self.user_type_name = data["nombre_tipo_usuario"]
        

    @classmethod
    def get_all(cls):
        table = "tipos_de_usuarios"
        query = "SELECT * FROM {};".format(table)
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
