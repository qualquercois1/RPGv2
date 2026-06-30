import sqlite3
from database import get_connection

class Item:
    def __init__(self, character_id, name, description="", item_type="Geral", quantity=1, weight=0.0, rarity="Comum", is_equipped=0, item_id=None):
        self.id = item_id,
        self.character_id = character_id,
        self.name = name
        self.description = description
        self.item_type = item_type
        self.quantity = quantity
        self.weight = weight
        self.rarity = rarity
        self.is_equipped = is_equipped

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO inventory (
                    character_id, name, description, item_type, 
                    quantity, weight, rarity, is_equipped
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.character_id, self.name, self.description, self.item_type,self.quantity, self.weight, self.rarity, self.is_equipped))
            self.id = cursor.lastrowid
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar o item: {e}")
            return False
        finally:
            conn.close()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM inventory WHERE id = ?', (self, id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar o item: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def get_inventory_by_character(cls, character_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM inventory WHERE character_id = ?', (character_id,))
        rows = cursor.fetchall()
        conn.close()
        
        inventory_list = []
        for row in rows:
            item = cls(
                item_id=row[0],
                character_id=row[1],
                name=row[2],
                description=row[3],
                item_type=row[4],
                quantity=row[5],
                weight=row[6],
                rarity=row[7],
                is_equipped=row[8]
            )
            inventory_list.append(item)
        return inventory_list
            
