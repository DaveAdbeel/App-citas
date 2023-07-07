from config import _DB as db
from utils.db_connection import connectToMySQL


class Discussions:
    def __init__(self, data):
        self.discussion_id = data["id_debate"]
        self.user_id = data["id_usuario"]
        self.title = data["titulo"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def insert_discussion(cls, data):
        try:
            table = "debates"
            query = f"""insert into `{table}` (id_usuario, titulo)
            values ("{data['user_id']}", "{data['title']}")
           """
            connectToMySQL(db).query_db(query)

        except Exception as e:
            raise Exception(f"Error {e}")

    @classmethod
    def get_all_discussions(cls):
        try:
            query = """ 
            SELECT 
              u.nombre AS nombre_usuario,
              u.id AS id_usuario,
              d.id_debate as id_debate,
              d.titulo AS titulo_debate,
              d.created_at AS fecha_creacion,
              d.updated_at AS fecha_actualizado,
              CASE
                WHEN c.id_comentario IS NULL THEN 'No hay ningún comentario'
                ELSE CONCAT(u2.nombre, ' - ', c.id_usuario, ' ', c.created_at, ' - ', c.contenido)
              END AS comentarios
            FROM usuarios u
            JOIN debates d ON u.id = d.id_usuario
            LEFT JOIN comentarios c ON d.id_debate = c.id_debate
            LEFT JOIN usuarios u2 ON c.id_usuario = u2.id
            ORDER BY d.id_debate, c.id_comentario;
            """
            
            result = connectToMySQL(db).query_db(query)
            
            return result
        
        except Exception as e:
            raise Exception(f"Error {e}")
    
    @classmethod
    def filter_discussions(self, data):
        debates = []
        debate_actual = None

        for item in data:
            if 'id_debate' in item:
                if item['id_debate'] != debate_actual:
                    if debate_actual is not None:
                        debates.append(debate)
                    debate = {
                        'nombre_usuario': item['nombre_usuario'],
                        'id_usuario': item['id_usuario'],
                        'id_debate': item['id_debate'],
                        'titulo_debate': item['titulo_debate'],
                        'fecha_creacion': item['fecha_creacion'],
                        'fecha_actualizado': item['fecha_actualizado'],
                        'comentarios': []
                    }
                    debate_actual = item['id_debate']
                if item['comentarios'] != 'No hay ningún comentario':
                    comentario_parts = item['comentarios'].split(' - ')
                    nombre_usuario, id_usuario, contenido = comentario_parts[0], comentario_parts[1].split()[0], comentario_parts[2]
                    comentario = {
                        'nombre_usuario': nombre_usuario,
                        'id_usuario': int(id_usuario),
                        'contenido': contenido
                    }
                    debate['comentarios'].append(comentario)
            else:
                print(f"La clave 'id_debate' no existe en el diccionario: {item}")

        if debate_actual is not None:
            debates.append(debate)

        return debates