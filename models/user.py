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

    @classmethod
    def get_passwd_hash(self, email):
        try:
            table = "usuarios"
            query = f"""
            select contraseña from {table} where email = '{email}'
            """
            result = connectToMySQL(db).query_db(query)
            contraseña = result[0]["contraseña"]
            
            return contraseña
            
        except Exception as e:
            raise Exception(f"Error: {e}") 
    
    @classmethod
    def get_user(self, email):  
        try:
            query = f"""
            select 
	        u.id, 
	        u.nombre, 
	        u.email, 
            tipos_de_usuarios.nombre_tipo_usuario as tipo_usuario, 
            sexo_de_interes.nombre_sexo as sexo_interes,
            (select count(titulo) from debates where debates.id_usuario = u.id) as discusiones,
            (select count(contenido) from comentarios where comentarios.id_usuario = u.id) as comentarios
            from usuarios as u
            JOIN tipos_de_usuarios ON tipos_de_usuarios.id = id_tipo_de_usuario
            JOIN sexo_de_interes ON sexo_de_interes.id = id_interes_sexo
            where email = '{email}';
            """
            result = connectToMySQL(db).query_db(query)
            user = result[0]
            return user
            
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    @classmethod
    def get_user_with_uid(self, uid):  
        try:
            query = f"""
            select 
	        u.id, 
	        u.nombre, 
	        u.email, 
            tipos_de_usuarios.nombre_tipo_usuario as tipo_usuario, 
            sexo_de_interes.nombre_sexo as sexo_interes,
            (select count(titulo) from debates where debates.id_usuario = u.id) as discusiones,
            (select count(contenido) from comentarios where comentarios.id_usuario = u.id) as comentarios
            from usuarios as u
            JOIN tipos_de_usuarios ON tipos_de_usuarios.id = id_tipo_de_usuario
            JOIN sexo_de_interes ON sexo_de_interes.id = id_interes_sexo
            where u.id = '{uid}';
            """
            result = connectToMySQL(db).query_db(query)
            user = result[0]
            return user
            
        except Exception as e:
            raise Exception(f"Error: {e}")
            
    @classmethod
    def update_user(self, user_id, username, email, password):
        try:
            if password != "":
                query = f"""
                UPDATE usuarios
                SET nombre = '{username}', email = '{email}', contraseña = "{password}"
                WHERE id = {user_id};
                """
            else:
                query = f"""
                UPDATE usuarios
                SET nombre = '{username}', email = '{email}'
                WHERE id = {user_id};
                """
                
            connectToMySQL(db).query_db(query)
        except Exception as e:
            raise Exception(f"Error: {e}")
            