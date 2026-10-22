import sqlite3
conn = sqlite3.connect('C:/Users/CBN/Desktop/SantaMartaSegura/backend/santamarta.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(lugares)')
print("Lugares columns:", cursor.fetchall())
cursor.execute('PRAGMA table_info(alertas)')
print("Alertas columns:", cursor.fetchall())
cursor.execute('PRAGMA table_info(emergencias)')
print("Emergencias columns:", cursor.fetchall())