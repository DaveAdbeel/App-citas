from config import _DB as db
from utils.db_connection import connectToMySQL


class Comments:
    def __init__(self, data):
        self.comment_id = data["id_comentario"]
        self.user_id = data["id_usuario"]
        self.discussion_id = data["id_debate"]
        self.content = data["contenido"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    @classmethod
    def insert_comment(self, data):
        try:
            table = "comentarios"
            query = f"""insert into {table} (id_usuario,contenido, id_debate) 
                        values ({data["user_id"]} , "{data["content"]}" , {data["discussion_id"]})
           """
            connectToMySQL(db).query_db(query)

        except Exception as e:
            raise Exception(f"Error {e}")
        
    @classmethod
    def edit_comment(self, uid, content):
        try:
            query = f"""update comentarios set contenido = "{content}", updated_at = NOW() WHERE id_comentario = {uid};"""
            
            connectToMySQL(db).query_db(query)

        except Exception as e:
            raise Exception(f"Error {e}")
        
    @classmethod
    def get_comment(self, uid):
        try:
            query = f"""select contenido from comentarios where id_comentario = {uid};"""
            
            result = connectToMySQL(db).query_db(query)
            return result[0]
        except Exception as e:
            raise Exception(f"Error {e}")
        
    @classmethod
    def delete_comment(self, uid):
        try:
            query = f"""delete from likes_usuarios where id_comentario = {uid};"""
            connectToMySQL(db).query_db(query)
            query = f"""delete from comentarios where id_comentario = {uid};"""
            connectToMySQL(db).query_db(query)
        except Exception as e:
            raise Exception(f"Error {e}")