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
    def insert_discussion(self, data):
        try:
            
            query = f"""insert into debates (id_usuario, titulo)
            values ("{data['user_id']}", "{data['title']}")
           """
            connectToMySQL(db).query_db(query)

        except Exception as e:
            raise Exception(f"Error {e}")
        
    @classmethod
    def delete_comments_for_discussion(self, uid):
        try:
            query = f"""select * from comentarios where id_debate = {uid};"""
            result = connectToMySQL(db).query_db(query)
            for comment in  result:
                query = f"""delete from likes_usuarios where id_comentario = {comment["id_comentario"]}"""
                connectToMySQL(db).query_db(query)
            query = f"""delete from comentarios where id_debate = {uid};"""
            connectToMySQL(db).query_db(query)

        except Exception as e:
            raise Exception(f"Error {e}")
    @classmethod
    def delete_discussion(self, uid):
        try:
            query = f"""delete from likes_usuarios where id_debate = {uid};"""
            connectToMySQL(db).query_db(query)
            self.delete_comments_for_discussion(uid)
            query = f"""delete from debates where id_debate = {uid}"""
            connectToMySQL(db).query_db(query)
        
        except Exception as e:
            raise Exception(f"Error {e}")
    
    @classmethod
    def edit_discussion(self, uid, title):
        try:
            query = f"""update debates set titulo = "{title}", updated_at = NOW() WHERE id_debate = {uid};"""
            
            connectToMySQL(db).query_db(query)
            
        except Exception as e:
            raise Exception(f"Error {e}")
    
    @classmethod
    def get_discussion(self, uid):
        try:
            query = f"""select titulo from debates where id_debate = {uid};"""
            result = connectToMySQL(db).query_db(query)
            return result[0]
        except Exception as e:
            raise Exception(f"Error {e}")

    @classmethod
    def get_all_discussions(self):
        try:
            query = """ 
            SELECT 
              u.nombre AS nombre_usuario,
              u.id AS id_usuario,
              d.id_debate as id_debate,
              d.titulo AS titulo_debate,
              d.created_at AS fecha_creacion,
              d.updated_at AS fecha_actualizado,
              d.me_gusta as me_gusta,
              CASE
                WHEN c.id_comentario IS NULL THEN 'No hay ningún comentario'
                ELSE CONCAT(u2.nombre, ' - ', c.id_usuario, ' - ', c.contenido, ' - ', c.id_comentario, ' - ', c.updated_at, ' - ', c.me_gusta)
              END AS comentarios
            FROM usuarios u
            JOIN debates d ON u.id = d.id_usuario
            LEFT JOIN comentarios c ON d.id_debate = c.id_debate
            LEFT JOIN usuarios u2 ON c.id_usuario = u2.id
            ORDER BY d.id_debate desc, c.id_comentario
            LIMIT 100
            """
            result = connectToMySQL(db).query_db(query)
            return result
        
        except Exception as e:
            raise Exception(f"Error {e}")
    
    @classmethod
    def filter_discussions(self, data):
        import datetime
        def convertir_fecha(fecha):
            ahora = datetime.datetime.now()
            tiempo_transcurrido = ahora - fecha

            segundos = tiempo_transcurrido.total_seconds()
            if segundos < 60:
                return f"Hace {int(segundos)} segundos"

            minutos = segundos / 60
            if minutos < 60:
                return f"Hace {int(minutos)} minutos"

            horas = minutos / 60
            if horas < 1:
                return f"Hace {int(horas)} horas"

            dias = horas / 24
            if dias < 7:
                return f"Hace {int(dias)} días"

            semanas = dias / 7
            if semanas < 4:
                return f"Hace {int(semanas)} semanas"

            meses = dias / 30.436875  # Promedio de días en un mes
            if meses < 12:
                return f"Hace {int(meses)} meses"

            años = meses / 12
            return f"Hace {int(años)} años"

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
                        'me_gusta': item["me_gusta"],
                        'comentarios': []
                    }
                    debate_actual = item['id_debate']
                if item['comentarios'] != 'No hay ningún comentario':
                    comentario_parts = item['comentarios'].split(' - ')
                    nombre_usuario, id_usuario, contenido, id_comentario, me_gusta = comentario_parts[0], comentario_parts[1].split()[0], comentario_parts[2], comentario_parts[3],comentario_parts[-1]
                    comentario = {
                        'nombre_usuario': nombre_usuario,
                        'id_usuario': int(id_usuario),
                        'contenido': contenido,
                        'id_comentario': int(id_comentario),
                        'me_gusta': int(me_gusta)                
                    }
                    debate['comentarios'].append(comentario)
            else:
                print(f"La clave 'id_debate' no existe en el diccionario: {item}")
        
        for dato in debates:
            fecha_creacion = dato['fecha_creacion']
            fecha_actualizado = dato['fecha_actualizado']

            fecha_creacion_dinamica = convertir_fecha(fecha_creacion)
            fecha_actualizado_dinamica = convertir_fecha(fecha_actualizado)

            dato['fecha_creacion'] = fecha_creacion_dinamica
            dato['fecha_actualizado'] = fecha_actualizado_dinamica
            
        


        if debate_actual is not None:
            fecha_creacion_dinamica = convertir_fecha(debate["fecha_creacion"])
            fecha_actualizado_dinamica = convertir_fecha(debate["fecha_actualizado"])

            debate["fecha_creacion"] = fecha_creacion_dinamica
            debate["fecha_actualizado"] = fecha_actualizado_dinamica
            
            debates.append(debate)

        return debates