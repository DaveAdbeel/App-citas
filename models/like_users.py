from config import _DB as db
from utils.db_connection import connectToMySQL


class Like_Users:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["id_usuario"]
        self.discussion_id = data["id_debate"]
        self.comment_id = data["id_comentario"]

    @classmethod
    def is_user_liked(self, user_id, query_type, discussion_id=None, comment_id=None):
        try:
            if query_type == "comment":
                
                query = f"""
                    select * from likes_usuarios 
                    where id_usuario = {user_id} and id_comentario = {comment_id}  
                """
            elif query_type == "discussion":
                query = f"""
                    select * from likes_usuarios 
                    where id_usuario = {user_id} and id_debate = {discussion_id}  
                """
                        
            result = connectToMySQL(db).query_db(query)
            print(result)
            if result == (): return False
            return True
        
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    @classmethod
    def handleLike(self, query_type, user_id_post, table, post_id, my_user_id):
        try:
            if query_type == "like":
                
                if table == "debates":
                    query = f"""
                        insert into likes_usuarios ( id_usuario, id_debate ) values ({my_user_id}, {post_id})
                    """
                    
                elif table == "comentarios":
                     query = f"""
                        insert into likes_usuarios ( id_usuario, id_comentario ) values ({my_user_id}, {post_id})
                    """    
                
                connectToMySQL(db).query_db(query)
                
                query = f"""UPDATE {table}
                            SET me_gusta = me_gusta + 1
                            WHERE id_{table[0:-1]} = {post_id}; """            
                connectToMySQL(db).query_db(query)
                query = f"""
                    UPDATE usuarios
                    set me_gusta = me_gusta + 1
                    where id = {user_id_post};
                """
                connectToMySQL(db).query_db(query)
                
            else:
                if table == "debates":
                    query = f"""
                    UPDATE likes_usuarios
                    SET id_debate = NULL
                    where id_debate = {post_id};
                """
                    connectToMySQL(db).query_db(query)
                elif table == "comentarios":
                    query = f"""
                    UPDATE likes_usuarios
                    SET id_comentario = NULL
                    where id_comentario = {post_id};
                """
                connectToMySQL(db).query_db(query)
                query = f"""UPDATE {table}
                            SET me_gusta = me_gusta - 1
                            WHERE id_{table[0:-1]} = {post_id}; """ 
                             
                connectToMySQL(db).query_db(query)

                query = f"""UPDATE usuarios
                            SET me_gusta = me_gusta - 1
                            WHERE id = {user_id_post}; """ 
                connectToMySQL(db).query_db(query)
        except Exception as e:
            raise  Exception(f"Error: {e}")