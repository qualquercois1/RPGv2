import streamlit as st
from database import get_connection

class Character:
    def __init__(self, user_id, name, age, eye_color, skin_color, classe, height, physical, race, region, attribute_strength, attribute_agility, attribute_vitality, attribute_intelligence,
                 attribute_survival, attribute_magic, character_id=None):
        self.id = character_id
        self.user_id = user_id
        self.name = name
        self.age = age
        self.eye_color = eye_color
        self.skin_color = skin_color
        self.classe = classe
        self.height = height
        self.physical = physical
        self.race = race
        self.region = region
        self.attribute_strength = attribute_strength
        self.attribute_agility = attribute_agility
        self.attribute_vitality = attribute_vitality
        self.attribute_intelligence = attribute_intelligence
        self.attribute_survival = attribute_survival
        self.attribute_magic = attribute_magic

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                           INSERT INTO characters (
                            user_id,
                            name,
                            age,
                            eye_color,
                            skin_color,
                            classe,
                            height,
                            physical,
                            race,
                            region,
                            attribute_strength,
                            attribute_agility,
                            attribute_vitality,
                            attribute_intelligence,
                            attribute_survival,
                            attribute_magic
                           ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', 
                           (self.user_id, self.name, self.age, self.eye_color, self.skin_color, self.classe, self.height, self.physical, self.race, self.region, self.attribute_strength, self.attribute_agility, self.attribute_vitality, self.attribute_intelligence, self.attribute_survival, self.attribute_magic))
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"Ocorreu um erro ao salvar o personagem: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def get_character_by_id(cls, character_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(
                character_id=row[0], user_id=row[1], name=row[2], age=row[3],
                eye_color=row[4], skin_color=row[5], classe=row[6], height=row[7],
                physical=row[8], race=row[9], region=row[10], attribute_strength=row[11],
                attribute_agility=row[12], attribute_vitality=row[13], attribute_intelligence=row[14],
                attribute_survival=row[15], attribute_magic=row[16]
            )
        return None