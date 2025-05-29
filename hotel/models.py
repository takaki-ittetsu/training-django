from django.db import models, connection
import logging

# =============
# Def
# =============

class HotelModel(models.Model):
    name = models.CharField(max_length=100)
    prefecture = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}_{self.name}"

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# =============
# RoomManager
# =============

class RoomManager:
    @classmethod
    def get_rooms_by_hotel_id(cls, hotel_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, hotel_id
                FROM rooms
                WHERE hotel_id = %s
            """, [hotel_id])
            return dictfetchall(cursor)
        
    @classmethod
    def create_room(cls, name, hotel_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO rooms (name, hotel_id)
                VALUES (%s, %s)
                RETURNING id
            """, [name, hotel_id])

            return cursor.fetchone()[0]
        
    @classmethod
    def get_room_by_id(cls, room_id):
        # Get Room By id
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, hotel_id
                FROM rooms          
                WHERE id = %s""", [room_id])
            
            results = dictfetchall(cursor)

            return results[0] if results else None
        
    @classmethod
    def update_room(cls, room_id, name):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE rooms
                SET name = %s
                WHERE id = %s
                RETURNING id
            """, [name, room_id])

            return cursor.fetchone()[0]
        
    @classmethod
    def delete_room(cls, room_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM rooms          
                WHERE id = %s
                RETURNING id
            """, [room_id])
            
            result = cursor.fetchone()
            return result[0] if result else None
        

# =============
# HotelManager
# =============

class HotelManager:
    @classmethod
    def get_all_hotels(cls):
        # Get All Hotels
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, prefecture
                FROM hotels
            """)
            return dictfetchall(cursor)
    
    @classmethod
    def get_hotel_by_id(cls, hotel_id):
        # Get Hotel By id
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, prefecture
                FROM hotels          
                WHERE id = %s""", [hotel_id])
            
            results = dictfetchall(cursor)

            if not results:
                return None
            
            hotel = results[0]
            hotel['rooms'] = RoomManager.get_rooms_by_hotel_id(hotel_id)

            return hotel
        
    @classmethod
    def create_hotel(cls, name, prefecture):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO hotels (name, prefecture)
                VALUES (%s, %s)
                RETURNING id
            """, [name, prefecture])

            return cursor.fetchone()[0]

    @classmethod
    def update_hotel(cls, hotel_id, name, prefecture):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE hotels
                SET name = %s, prefecture = %s
                WHERE id = %s
                RETURNING id
            """, [name, prefecture, hotel_id])

            return cursor.fetchone()[0]
        
    @classmethod
    def delete_hotel(cls, hotel_id):
        rooms = RoomManager.get_rooms_by_hotel_id(hotel_id)
        for room in rooms:
            RoomManager.delete_room(room['id'])

        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM hotels          
                WHERE id = %s
                RETURNING id
            """, [hotel_id])
            
            result = cursor.fetchone()
            return result[0] if result else None