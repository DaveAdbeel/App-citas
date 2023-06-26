from config import _DB as db
from utils.db_connection import connectToMySQL


class Interest_Sex:
    def __init__(self, data):
        self.id = data["id"]
        self.sex_name = data["nombre_sexo"]
        

    @classmethod
    def get_all(cls):
        table = "sexo_de_interes"
        query = "SELECT * FROM {};".format(table)
        results = connectToMySQL(db).query_db(query)
        sexes = []
        for sex in results:
            sexes.append(cls(sex))
        return sexes
