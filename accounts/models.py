from django.db import connection

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class UserManager:
    @classmethod
    def create_user(cls, username, hashed_password):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            """, [username, hashed_password])
            return True
        
    @classmethod
    def get_user_by_username(cls, username):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, password
                FROM users
                WHERE username = %s
            """, [username])

            result = dictfetchall(cursor)
            return result[0] if result else None